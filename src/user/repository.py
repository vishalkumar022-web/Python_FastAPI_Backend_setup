# In this Repository file, we define functions that directly talk to the Database.
# Yahan sirf queries chalengi, koi HTTP/API errors handle nahi honge.

from src.user.model import UserModel 
from src.user.dtos import UserRequest
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

# Password hashing ka recommended object banaya
password_hash = PasswordHash.recommended()

def get_password_hash(password):
    # Plain password ko hash (encrypt) karne ke liye
    return password_hash.hash(password)

def register_user(db: Session, user_request: UserRequest):
    # Registration ke waqt password ko hash karke DB me daal rahe hain
    new_hashed_password = get_password_hash(user_request.hash_password)
   
    user = UserModel(
        username=user_request.username,
        name=user_request.name,
        email=user_request.email,
        hash_password=new_hashed_password,
        mobile_number=user_request.mobile_number
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_all_users(db: Session):
    return db.query(UserModel).all()

def delete_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def update_user(db: Session, user_id: int, user_request: UserRequest):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        updated_data = user_request.model_dump()
        for key, value in updated_data.items():
            setattr(user, key, value)
       
       
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return None

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user_by_mobile(db: Session, mobile: int):
    return db.query(UserModel).filter(UserModel.mobile_number == mobile).first()

def get_user_by_username(db: Session, username: str):
    # Username se user dhundhne ka simple function
    return db.query(UserModel).filter(UserModel.username == username).first()


def verify_password(plain_password, hashed_password):
    # Try-except block lagaya hai taaki agar purana/plain-text password mile 
    # toh server 500 error dekar crash na ho, balki properly 401 Unauthorized de.
    try:
        return password_hash.verify(plain_password, hashed_password)
    except Exception as e:
        # Agar hash ka format galat hai (jaise seedha "1234" likha hai DB me)
        return False
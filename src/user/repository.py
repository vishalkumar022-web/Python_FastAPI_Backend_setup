from src.user.model import UserModel 
from src.user.dtos import UserRequest
from sqlalchemy.orm import Session
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

 
def get_password_hash(password):
    return password_hash.hash(password)



def register_user(db: Session, user_request: UserRequest):
   
    new_hashed_password = get_password_hash(user_request.hash_password)
   
    user = UserModel(
        username=user_request.username,
        name=user_request.name,
        email=user_request.email,
        hash_password= new_hashed_password ,
        mobile_number=user_request.mobile_number
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def get_user_by_id(db:Session , user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()



def get_all_users(db:Session):
    return db.query(UserModel).all()



def delete_user(db:Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False



def update_user(db:Session, user_id: int, user_request: UserRequest):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if user:
        updated_data = user_request.model_dump()
        for key, value in updated_data.items():
            setattr(user, key, value)
            
        # Commit aur refresh loop ke BAHAR hona chahiye
        db.commit()
        db.refresh(user)
        return user
    return None



def get_user_by_email(db: Session , email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_mobile(db: Session , mobile: int):
    return db.query(UserModel).filter(UserModel.mobile_number == mobile).first()

def get_user_by_username(db, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()
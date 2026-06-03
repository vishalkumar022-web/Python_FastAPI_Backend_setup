from src.user.model import UserModel 
from src.user.dtos import UserRequest

def register_user(db, user_request: UserRequest):
    user = UserModel(
        username=user_request.username,
        name=user_request.name,
        email=user_request.email,
        hash_password=user_request.hash_password,
        mobile_number=user_request.mobile_number
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_all_users(db):
    return db.query(UserModel).all()

def delete_user(db, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
    
def update_user(db, user_id: int, user_request: UserRequest):
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

def get_user_by_email(db, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user_by_mobile(db, mobile: int):
    return db.query(UserModel).filter(UserModel.mobile_number == mobile).first()

def get_user_by_username(db, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()
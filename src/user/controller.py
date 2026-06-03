from src.user.dtos import UserRequest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.user import repository

def register_user(body: UserRequest, db: Session):
    # 1. username validate karna hai
    user_with_same_username = repository.get_user_by_username(db, body.username)
    if user_with_same_username:
        raise HTTPException(status_code=400, detail="Username already exists!")

    # 2. email validate karna hai
    user_with_same_email = repository.get_user_by_email(db, body.email)
    if user_with_same_email:
        raise HTTPException(status_code=400, detail="Email already exists!")

    # 3. mobile number validate karna hai (Yahan body.mobile ko fix kiya)
    user_with_same_mobile = repository.get_user_by_mobile(db, body.mobile_number)
    if user_with_same_mobile:
        raise HTTPException(status_code=400, detail="Mobile number already exists!")

    # Repository call pattern theek kiya -> (db, body)
    new_user = repository.register_user(db, body)

    if not new_user:
        raise HTTPException(status_code=400, detail="User registration failed!")
    
    return new_user


def get_user_by_id(id: int, db: Session):
    user = repository.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return user

def get_all_users(db: Session):
    users = repository.get_all_users(db) # function naam lowercase match kiya
    if not users:
        raise HTTPException(status_code=404, detail="No users found!")
    return users

def delete_user(id: int, db: Session):
    result = repository.delete_user(db, id)
    if not result:
        raise HTTPException(status_code=400, detail="User deletion failed or not found!")
    return None

def update_user(id: int, body: UserRequest, db: Session):
    updated_user = repository.update_user(db, id, body)
    if not updated_user:
        raise HTTPException(status_code=400, detail="User update failed or not found!")
    return updated_user
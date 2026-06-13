# In this Controller file, we handle the validation, business logic, and raise HTTP errors.
# Ye file sirf inputs check karegi aur Repository ko instructions degi.

from src.user.dtos import UserRequest, loginRequest
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.user import repository
from src.utils.settings import settings
from datetime import datetime, timedelta
import jwt

def register_user(body: UserRequest, db: Session):
    user_with_same_username = repository.get_user_by_username(db, body.username)
    if user_with_same_username:
        raise HTTPException(status_code=400, detail="Username already exists!")

    user_with_same_email = repository.get_user_by_email(db, body.email)
    if user_with_same_email:
        raise HTTPException(status_code=400, detail="Email already exists!")

    user_with_same_mobile = repository.get_user_by_mobile(db, body.mobile_number)
    if user_with_same_mobile:
        raise HTTPException(status_code=400, detail="Mobile number already exists!")

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
    users = repository.get_all_users(db)
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




def login_user(body: loginRequest, db: Session):
    # 1. Pehle database se username check karo
    user = repository.get_user_by_username(db, body.username)
    
    # FIX: Agar user database me NAHI mila, tab error raise karna hai!
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Username is not found in DB you are given a wrong username !"
        )

    # 2. Agar user mil gaya, toh password verify karo
    verification_of_Password = repository.verify_password(body.hash_password, user.hash_password)

    if not verification_of_Password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Given password is not found for this User you are given a wrong password for this user !"
        )

    # 3. Agar dono sahi hain, toh JWT Token generate karo
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    
    token = jwt.encode(
        {"id": user.id, "exp": exp_time}, 
        settings.SECRET_KEY, 
        settings.ALGORITHM
    )

    return {"token": token}
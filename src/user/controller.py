# In this Controller file, we handle the validation, business logic, and raise HTTP errors.
# Ye file sirf inputs check karegi aur Repository ko instructions degi.

from src.user.dtos import UserRequest, loginRequest
from sqlalchemy.orm import Session
from fastapi import HTTPException, status , Request , BackgroundTasks
from src.user import repository
from src.utils.settings import settings
from datetime import datetime, timedelta

# Imports ko aise theek kar lo:
from src.utils.mail import send_email, send_otp_email
import random

import uuid

from src.user.model import UserModel


from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from src.user.dtos import GoogleLoginRequest
# settings se GOOGLE_CLIENT_ID import karna mat bhoolna



import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi.security import HTTPAuthorizationCredentials # Ye token ko securely handle karega




# Function me 'background_tasks' parameter add kiya
async def register_user(body: UserRequest, background_tasks: BackgroundTasks, db: Session):
    
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
    
    # -------------------------------------------------------------
    # FIX: Email bhejne ka kaam background ko de diya! 
    # API yahan wait nahi karegi, turant user ko response de degi.
    # -------------------------------------------------------------
    background_tasks.add_task(send_email, [new_user.email])

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
    
    # FIX: .strip() lagaya hai taaki agar user galti se space type kar de, toh wo hat jaye
    clean_username = body.username.strip()
    
    # Ab DB me clean_username search karenge
    user = repository.get_user_by_username(db, clean_username)
    
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
        {"id": user.id, "exp": exp_time.timestamp()}, 
        settings.SECRET_KEY, 
        settings.ALGORITHM
    )

    return {"User Details ":user ,"token": token}

## Token send :---


# ... (baaki ka tumhara register, login ka code waise hi rahega) ...

## Token Verify & User Extract karne ka function :---
def is_authenticated(credentials: HTTPAuthorizationCredentials, db: Session):
    try:
        # 1. credentials.credentials apne aap "Bearer " word ko hata kar sirf main token nikal leta hai.
        # Humein token.split(" ") karne ki zaroorat nahi hai ab!
        token = credentials.credentials

        # 2. Token ko decode karna
        # PyJWT apne aap check kar leta hai ki token expire (exp) hua hai ya nahi.
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # 3. Payload se user ki ID nikalna (Pichli baar tumne "_id" likha tha, jabki humne "id" save kiya tha)
        user_id = data.get("id")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token Payload")
        
        # 4. Database se check karna ki ye user abhi bhi exist karta hai ya nahi
        user = repository.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found! Unauthorized")
        
        # Agar sab kuch theek hai, toh user return kar do
        return user 

    # Agar token ka time (exp) nikal chuka hai, toh ye error aayega
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired. Please login again.")
    
    # Agar kisi ne token ke sath chhed-chhad ki hai ya galat token diya hai
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token! You are Unauthorized")
    




async def handle_forgot_password(request_data, background_tasks: BackgroundTasks, db_session: Session):
       # 1. Repository se user find karo
       user = repository.get_user_by_email(db_session, request_data.email)
       if not user:
           raise HTTPException(status_code=404, detail="Email not found!")

       # 2. 6-digit random OTP generate karo aur Expiry time (5 mins) set karo
       otp = str(random.randint(100000, 999999))
       expiry_time = datetime.now() + timedelta(minutes=5)

       # 3. Repository ke through DB me OTP save karo
       repository.save_otp(db_session, user, otp, expiry_time)

       # 4. Background task me email bhej do (taaki API fast chale)
       background_tasks.add_task(send_otp_email, user.email, otp)
       
       return {"message": "OTP sent successfully to your email"}


async def handle_reset_password(request_data, db_session: Session):
       # 1. Repository se user find karo
       user = repository.get_user_by_email(db_session, request_data.email)
       if not user:
           raise HTTPException(status_code=404, detail="User not found")

       # 2. Check karo OTP match ho raha hai aur expire toh nahi hua
       if user.reset_otp != request_data.otp:
           raise HTTPException(status_code=400, detail="Invalid OTP")
       
       if datetime.now() > user.otp_expiry:
           raise HTTPException(status_code=400, detail="OTP has expired")

       # 3. Repository ke through password reset karo (wo khud hash karke save kar lega)
       repository.reset_user_password(db_session, user, request_data.new_password)

       return {"message": "Password reset successfully!"}




async def google_login(request_data: GoogleLoginRequest, db_session: Session):
    try:
        # 1. Google token verify karo
        id_info = id_token.verify_oauth2_token(
            request_data.token, 
            google_requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )

        # 2. Google se user ki details nikalo
        email = id_info.get("email")
        name = id_info.get("name")

        # 3. Check karo DB me user hai ya nahi
        user = repository.get_user_by_email(db_session, email)

        if not user:
            # Username ko unique banane ka mast tarika
            base_username = email.split("@")[0]
            unique_username = f"{base_username}_{random.randint(1000, 9999)}"

            # Agar naya user hai, toh DB me save karo (bina password/mobile ke)
            new_user_data = UserModel(
                username=unique_username,
                name=name,
                email=email,
                hash_password=None, 
                mobile_number=None,
                is_active=True
            )
            # YEH SAARI LINES 'if' BLOCK KE ANDAR HONI CHAHIYE
            db_session.add(new_user_data)
            db_session.commit()
            db_session.refresh(new_user_data)
            user = new_user_data # Ab user update ho gaya

        # 4. Apna JWT token banao aur bhej do
        exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
        token = jwt.encode(
            {"id": user.id, "exp": exp_time.timestamp()}, 
            settings.SECRET_KEY, 
            settings.ALGORITHM
        )

        return {"User Details": user, "token": token}
    
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google Token!")
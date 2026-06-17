from pydantic import BaseModel
from datetime import datetime

class UserRequest(BaseModel):
    username: str
    name: str
    email: str
    hash_password: str
    mobile_number: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    mobile_number: str
    created_at: datetime # Isko string se datetime kar diya
    is_active: bool



class loginRequest(BaseModel):
    username : str 
    hash_password: str


class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    otp: str
    new_password: str
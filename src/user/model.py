from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from src.utils.db import Base 

class UserModel(Base):
    __tablename__ = "user_table" 

    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String, unique=True, index=True, nullable=False) 
    name = Column(String, nullable=False) 
    email = Column(String, unique=True, index=True, nullable=False) 
    hash_password = Column(String, nullable=False) 


   # <-- Yahan Integer ko String se replace kar diya!
    mobile_number = Column(String, unique=True, index=True, nullable=False)
    
    
    # Yahan default time add kiya, taaki DB khud time daal de
    created_at = Column(DateTime, default=func.now()) 
    is_active = Column(Boolean, default=True)


    # Tumhari User class ke andar ye add karna hai:
    reset_otp = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
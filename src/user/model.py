from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from src.utils.db import Base 

class UserModel(Base):
    __tablename__ = "user_table" 

    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String, unique=True, index=True, nullable=False) 
    name = Column(String, nullable=False) 
    email = Column(String, unique=True, index=True, nullable=False) 
   # model.py me changes
    hash_password = Column(String, nullable=True) # Pehle False tha

    mobile_number = Column(String, nullable=True) # Pehle False tha
    
    
    # Yahan default time add kiya, taaki DB khud time daal de
    created_at = Column(DateTime, default=func.now()) 
    is_active = Column(Boolean, default=True)


    # Tumhari User class ke andar ye add karna hai:
    reset_otp = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
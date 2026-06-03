

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.utils.db import Base # ye base responsible hai hamare models ko database ke tables me convert karne ke liye. Isko import karke ham apne Task model ko Base se inherit karenge, jisse hamare Task model ka structure database me ek table ke roop me create ho jayega.

class UserModel(Base):
    __tablename__ = "user_table" # ye line specify karti hai ki hamare UserModel ka data database me "users" naam ke table me store hoga. Isse hamare database me ek "users" naam ka table create ho jayega jisme hamare UserModel ke fields ke corresponding columns honge.

    id = Column(Integer, primary_key=True, index=True) # ye line define karti hai ki hamare UserModel me ek "id" field hoga jo Integer type ka hoga, primary key hoga aur index bhi hoga. Primary key hone ka matlab hai ki ye field unique hoga aur har record ke liye alag value hogi. Index hone ka matlab hai ki is field par database me indexing create ho jayegi, jisse queries ko faster banaya ja sakta hai.

    username = Column(String, unique=True, index=True , nullable= False) # ye line define karti hai ki hamare UserModel me ek "username" field hoga jo String type ka hoga, unique hoga aur index bhi hoga. Unique hone ka matlab hai ki is field me duplicate values allowed nahi hongi. Index hone ka matlab hai ki is field par database me indexing create ho jayegi, jisse queries ko faster banaya ja sakta hai.

    name = Column(String, nullable=False) # ye line define karti hai ki hamare UserModel me ek "name" field hoga jo String type ka hoga. Is field me user ke name ko store kiya jayega.

    email = Column(String, unique=True, index=True, nullable=False) # ye line define karti hai ki hamare UserModel me ek "email" field hoga jo String type ka hoga, unique hoga aur index bhi hoga. Unique hone ka matlab hai ki is field me duplicate values allowed nahi hongi. Index hone ka matlab hai ki is field par database me indexing create ho jayegi, jisse queries ko faster banaya ja sakta hai.

    hash_password = Column(String , nullable=False) # ye line define karti hai ki hamare UserModel me ek "hash_password" field hoga jo String type ka hoga. Is field me user ke password ko store kiya jayega.

    mobile_number = Column(Integer, unique=True, index=True, nullable=False) # ye line define karti hai ki hamare UserModel me ek "mobile_number" field hoga jo String type ka hoga, unique hoga aur index bhi hoga. Unique hone ka matlab hai ki is field me duplicate values allowed nahi hongi. Index hone ka matlab hai ki is field par database me indexing create ho jayegi, jisse queries ko faster banaya ja sakta hai.

    created_at = Column(DateTime) # ye line define karti hai ki hamare UserModel me ek "created_at" field hoga jo DateTime type ka hoga. Is field me user ke account creation date and time ko store kiya jayega.

    is_active = Column(Boolean, default=True) # ye line define karti hai ki hamare UserModel me ek "is_active" field hoga jo Boolean type ka hoga aur iska default value True hoga.


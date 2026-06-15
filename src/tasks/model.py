from sqlalchemy import Column, Integer, String, Boolean , ForeignKey

from src.utils.db import Base # ye base responsible hai hamare models ko database ke tables me convert karne ke liye. Isko import karke ham apne Task model ko Base se inherit karenge, jisse hamare Task model ka structure database me ek table ke roop me create ho jayega.


class TaskModel(Base):
    __tablename__ = "tasks" # ye line specify karti hai ki hamare TaskModel ka data database me "tasks" naam ke table me store hoga. Isse hamare database me ek "tasks" naam ka table create hoga jisme hamare TaskModel ke fields ke corresponding columns honge.

    id = Column(Integer, primary_key=True, index=True) # ye line define karti hai ki hamare TaskModel me ek "id" field hoga jo Integer type ka hoga, primary key hoga aur index bhi hoga. Primary key hone ka matlab hai ki ye field unique hoga aur har record ke liye alag value hogi. Index hone ka matlab hai ki is field par database me indexing create ho jayegi, jisse queries ko faster banaya ja sakta hai.


    title = Column(String, index=True) # ye line define karti hai ki hamare TaskModel me ek "title" field hoga jo String type ka hoga aur index bhi hoga. Index hone ka matlab hai ki is field par database me indexing create ho jayegi, jisse queries ko faster banaya ja sakta hai.


    description = Column(String) # ye line define karti hai ki hamare TaskModel me ek "description" field hoga jo String type ka hoga. Is field me task ke description ko store kiya jayega.

    
    status = Column(Boolean, default=False) # ye line define karti hai ki hamare TaskModel me ek "status" field hoga jo Boolean type ka hoga aur iska default value False hoga. Is field me task ke status ko store kiya jayega, jisme True ka matlab task complete hai aur False ka matlab task incomplete hai.


    # TaskModel ke andar ye line zaroor add karna bhai
    user_id = Column(Integer , ForeignKey("user_table.id" , ondelete= "CASCADE")) # Ye batayega ki ye task kis user ne banaya hai
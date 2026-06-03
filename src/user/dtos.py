
from pydantic import BaseModel # ye line pydantic library se BaseModel class ko import karti hai. Pydantic ek data validation aur settings management library hai jo Python me data models banane ke liye use hoti hai. BaseModel class ko inherit karke ham apne data models bana sakte hain, jisme ham apne fields ko define kar sakte hain aur unki types specify kar sakte hain. Pydantic automatically data validation aur parsing ka kaam karta hai, jisse hamare code me errors kam hote hain aur data consistency maintain hoti hai.    

class UserRequest(BaseModel):
    username: str
    name: str
    email: str
    hash_password: str
    mobile_number: int
    password: str



class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    mobile_number: int
    created_at: str
    is_active: bool
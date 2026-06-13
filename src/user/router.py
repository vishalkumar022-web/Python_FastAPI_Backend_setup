from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.user.dtos import UserRequest, UserResponse,loginRequest
from src.user import controller # Yahan poora controller import kiya
from src.utils.db import get_db

user_routes = APIRouter(prefix="/users")

@user_routes.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user_route(body: UserRequest, db: Session = Depends(get_db)):
    # Controller ka register function call hoga
    return controller.register_user(body, db)

@user_routes.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id_route(id: int, db: Session = Depends(get_db)):
    # Sahi function call karna zaroori hai!
    return controller.get_user_by_id(id, db)

@user_routes.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users_route(db: Session = Depends(get_db)):
    return controller.get_all_users(db)

@user_routes.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(id: int, db: Session = Depends(get_db)):
    return controller.delete_user(id, db)

@user_routes.put("/{id}", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def update_user_route(id: int, body: UserRequest, db: Session = Depends(get_db)):
    return controller.update_user(id, body, db)


@user_routes.post("/login" , status_code= status.HTTP_200_OK)
def login(body:loginRequest , db:Session = Depends(get_db)):

    return controller.login_user(body,db)
from fastapi import APIRouter, Depends, status, Request , BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Upar imports me in dono ko add kar lena
from src.user.dtos import UserRequest, UserResponse, loginRequest, ForgotPasswordRequest, ResetPasswordRequest

from src.user import controller
from src.utils.db import get_db

user_routes = APIRouter(prefix="/users")

# Security object for Swagger Lock Icon
security = HTTPBearer() 



@user_routes.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user_route(body: UserRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Controller ko background_tasks pass kar diya
    return await controller.register_user(body, background_tasks, db)


@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login(body: loginRequest, db: Session = Depends(get_db)):
    return controller.login_user(body, db)

@user_routes.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users_route(db: Session = Depends(get_db)):
    return controller.get_all_users(db)


# ==========================================
# FIX: /is_auth ko humne upar rakh diya!
# ==========================================
@user_routes.get("/is_auth", response_model=UserResponse, status_code=status.HTTP_200_OK)
def is_auth(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return controller.is_authenticated(credentials, db)


# ==========================================
# /{id} wala route HAMESHA specific routes ke niche hona chahiye
# ==========================================
@user_routes.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id_route(id: int, db: Session = Depends(get_db)):
    return controller.get_user_by_id(id, db)

@user_routes.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(id: int, db: Session = Depends(get_db)):
    return controller.delete_user(id, db)

@user_routes.put("/{id}", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def update_user_route(id: int, body: UserRequest, db: Session = Depends(get_db)):
    return controller.update_user(id, body, db)




@user_routes.post("/forgot-password")
async def forgot_password_route(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return await controller.handle_forgot_password(request, background_tasks, db)

@user_routes.post("/reset-password")
async def reset_password_route(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return await controller.handle_reset_password(request, db)
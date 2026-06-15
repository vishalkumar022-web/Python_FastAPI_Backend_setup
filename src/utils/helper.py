from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # Ye line zaroori hai
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from src.user import repository
from src.utils.settings import settings
from src.utils.db import get_db

# 1. Ye security object Swagger me Lock 🔒 banayega
security = HTTPBearer()

## Token Verify & User Extract karne ka function :---
# FIX: Yahan 'Depends(security)' lagana bohot zaroori tha, varna 422 error aayega!
def is_authenticated(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = data.get("id")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token Payload")
        
        user = repository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found! Unauthorized")
        
        return user # JWT valid hai, toh hum pura user object wapas de rahe hain

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired. Please login again.")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token! You are Unauthorized")
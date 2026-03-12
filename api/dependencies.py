from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import SessionLocal, get_db
from db import models
from core import security
import jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decode the token using your secret key
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        
        # 2. Block refresh tokens from being used as access tokens
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token type. Please use an access token."
            )
            
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception
        
    # 3. Verify the user still exists in the database
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user        
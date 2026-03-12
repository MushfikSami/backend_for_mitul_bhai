from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import get_current_user
from db import models
from db.database import get_db
from core import security
from schemas.schemas import UserResponse, UserCreate, Token, TokenRefreshRequest
import jwt

router=APIRouter()




@router.post('/register',response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user:UserCreate,db:Session=Depends(get_db)):
    user_model=db.query(models.User).filter(models.User.email==user.email).first()
    if user_model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Email already registered')
    hashed_password=security.get_hashed_password(user.password)
    new_user=models.User(email=user.email,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user    


@router.post('/login',response_model=Token)
def login(user:UserCreate,db:Session=Depends(get_db)):
    user_model=db.query(models.User).filter(models.User.email==user.email).first()
    if not user_model or not security.verify_password(user.password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid email or password')
    
    access_token=security.create_access_token(data={'sub':user_model.email})
    refresh_token=security.create_refresh_token(data={'sub':user_model.email})
    return {'access_token':access_token,'refresh_token':refresh_token,'token_type':'bearer'}


@router.post('/refresh',response_model=Token)
def refresh_token(request:TokenRefreshRequest,db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(request.refresh_token,security.SECRET_KEY,algorithms=[security.ALGORITHM])
        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid token type')
        email=payload.get('sub')
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid token payload')
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Refresh token expired')    
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid refresh token')
    

    user_model=db.query(models.User).filter(models.User.email==email).first()
    if not user_model:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not found')
    
    access_token=security.create_access_token(data={'sub':user_model.email})
    refresh_token=security.create_refresh_token(data={'sub':user_model.email})
    return {'access_token':access_token,'refresh_token':refresh_token,'token_type':'bearer'}



@router.get('/mitul')
def mitul(current_user: models.User = Depends(get_current_user)):
    return {'message':'Hello Mitul! You are authenticated.'}
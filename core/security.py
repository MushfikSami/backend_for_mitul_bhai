import jwt 
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY='MITULMUSHRATMOMODREAM71'
ALGORITHM='HS256'
TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=60*24*7

pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')


def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)


def get_hashed_password(password:str):
    return pwd_context.hash(password)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now()+timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire,'type':'access'})
    jwt_encode=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_encode

def create_refresh_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now()+timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire,'type':'refresh'})
    jwt_encode=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_encode
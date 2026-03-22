from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from config.settings import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from db.database import get_database
from bson import ObjectId


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict):
    to_encode = data.copy()
    exp = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN)
    to_encode.update({"exp":exp})
    access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return access_token

def create_refresh_token(data:dict):
    to_encode = data.copy()
    exp = datetime.now() + timedelta(days=settings.REFRESH_TOKEN)
    to_encode.update({"exp":exp})
    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return refresh_token

def decode_token(token:str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        userid = payload.get("sub")
        if not userid:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        return userid
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

async def get_current_user(token:str=Depends(oauth2_scheme), db=Depends(get_database)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        userid: str = payload.get("sub")
        if userid is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

    result = await db.user_details.find_one({"_id":ObjectId(userid)})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return result
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_services import UserCreate
from config.security import hash_password, create_access_token, create_refresh_token, verify_password, decode_token
from db.database import get_database
from datetime import datetime
from bson import ObjectId


router = APIRouter()

@router.post("/register")
async def get_register(user_request:UserCreate, db=Depends(get_database)):
    check_user = await db.user_details.find_one({"email":user_request.email}, {"_id":0})
    if check_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user_request.password)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    store_det = await db.user_details.insert_one({"email":user_request.email, "password":hashed_password, "created_at":created_at})
    if not store_det:
        return {"status_code":500, "message":"Data not inserted"}
    
    access_token = create_access_token({"sub":str(store_det.inserted_id)})
    refresh_token = create_refresh_token({"sub":str(store_det.inserted_id)})
    return {"access_token":access_token, "refresh_token":refresh_token}

@router.post("/login")
async def login(form_data:OAuth2PasswordRequestForm=Depends(), db=Depends(get_database)):
    check_user = await db.user_details.find_one({"email":form_data.username})
    if not check_user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    hashed_password = check_user.get("password")
    check_password = verify_password(form_data.password, hashed_password)
    if not check_password:
        raise HTTPException(status_code=400, detail="Invalid credential")
    
    access_token = create_access_token({"sub":str(check_user["_id"])})
    refresh_token = create_refresh_token({"sub":str(check_user["_id"])})
    return {"access_token":access_token, "refresh_token":refresh_token}

@router.post("/refresh")
async def refresh_access_token(token:str, db=Depends(get_database)):
    user_id = decode_token(token)

    user = await db.user_details.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token({"sub": user_id})
    return {"access_token": new_access_token}
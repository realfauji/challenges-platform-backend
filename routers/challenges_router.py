from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from db.database import get_database
from services.challenges_services import CreateChallenge, UpdateProgress
from datetime import datetime
from config.security import get_current_user
from bson import ObjectId


router = APIRouter()

@router.get("/get-challenges")
async def get_challenge(db=Depends(get_database)):
    active_challenge = await db.challenges.find({"is_active":True}).to_list(length=None)
    if not active_challenge:
        return {"status_code":400, "messages":"No active challenges"}
    
    challenges = []
    for challenge in active_challenge:
        challenge["_id"] = str(challenge["_id"])
        challenges.append(challenge)
        
    return challenges

@router.post("/create-challenges")
async def create_challenges(challenge_det:CreateChallenge, user=Depends(get_current_user), db=Depends(get_database)):
    post_data = jsonable_encoder(challenge_det)
    post_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    post_data["created_by"] = str(user["_id"])
    
    store_det = await db.challenges.insert_one(post_data)
    if not store_det.inserted_id:
        return {"status_code":500, "message":"Data not inserted"}
    
    return {"status_code":200, "message":"Challenge post created"}

@router.post("/{challenge_id}/join")
async def join_challenge(challenge_id: str, user=Depends(get_current_user), db=Depends(get_database)):
    check_exist_challenge = await db.challenges.find_one({"_id": ObjectId(challenge_id)})
    if not check_exist_challenge:
        return {"status_code":404, "detail":"challenge not found"}

    existing = await db.user_challenges.find_one({"user_id": str(user["_id"]),"challenge_id": challenge_id})
    if existing:
        return {"status_code":400, "detail":"Already joined"}

    record = {
        "user_id": str(user["_id"]),
        "challenge_id": challenge_id,
        "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "progress": 0
    }

    await db.user_challenges.insert_one(record)
    return {"status_code":200, "message":"Joined challenge"}

@router.put("/progress")
async def update_progress(update_progress: UpdateProgress, user=Depends(get_current_user), db=Depends(get_database)):
    progress_det = jsonable_encoder(update_progress)
    
    result = await db.user_challenges.update_one({"user_id": str(user["_id"]), "challenge_id": progress_det["challenge_id"]}, {"$set": {"progress": progress_det["progress_value"]}})
    if result.matched_count == 0:
        return {"status_code":404, "detail":"Record not found"}

    return {"status_code":200, "message": "Progress updated"}
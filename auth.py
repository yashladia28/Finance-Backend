from fastapi import Header, HTTPException
from bson import ObjectId
from database import users_collection


def get_current_user(x_user_id: str = Header(...)):
    try:
        user = users_collection.find_one({"_id": ObjectId(x_user_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user["role"]
from auth import get_current_user
from bson import ObjectId
from datetime import datetime
from database import users_collection, records_collection
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from models import UserCreate, UserOut, UserUpdate, RecordCreate, RecordOut, RecordUpdate
from typing import Optional, Literal
app = FastAPI(title="Finance Dashboard API", version="1.0.0")
def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Finance backend running"}

@app.post("/users")
def add_user(user: UserCreate,role: str = Depends(get_current_user)):
    if role not in ["admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    doc = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "role": user.role,
        "is_active": True,
        "created_at": datetime.now(),
    }
    
    users_collection.insert_one(doc)
    return {"message": "user created"}

@app.get("/users")
def get_user(role: str = Depends(get_current_user)):
    if role not in ["admin", "analyst","viewer"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    data = []
    for user in users_collection.find():
        doc = {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "is_active": user["is_active"],
            "created_at": user["created_at"],
        }
        data.append(doc)
    return data

@app.get("/users/{user_id}")
def get_user_by_id(user_id:str, role: str = Depends(get_current_user)):
    if role not in ["admin", "analyst","viewer"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = users_collection.find_one({"_id":validate_object_id(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "is_active": user["is_active"],
        "created_at": user["created_at"],
    }
@app.patch("/users/{user_id}")
def update_one(user_id: str,user: UserUpdate, role: str = Depends(get_current_user)):
    if role not in ["admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = users_collection.update_one(
        {"_id": validate_object_id(user_id)},
        {"$set":user.model_dump(exclude_none=True)}    
        )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "user updated"}

@app.delete("/users/{user_id}")
def delete_one(user_id:str, role: str = Depends(get_current_user)):
    if role not in ["admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = users_collection.delete_one({"_id":validate_object_id(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "user deleted"}

@app.post("/records")
def add_record(record: RecordCreate, created_by: str, role: str = Depends(get_current_user)):
    if role not in ["admin", "analyst"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    doc = {
        "title": record.title,
        "amount": record.amount,
        "type": record.type,
        "category": record.category,
        "date": record.date,
        "notes": record.notes,
        "created_by": created_by,          
        "created_at": datetime.now()
    }
    records_collection.insert_one(doc)
    return {"message": "record created"}

@app.get("/records")
def get_records(type: Optional[str] = None,page: Optional[int] = 1,limit: Optional[int] = 10, category: Optional[str] = None, date: Optional[str] = None, role: str = Depends(get_current_user)):
    if role not in ["admin", "analyst","viewer"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    query = {}
    skip = (page - 1) * limit
    if type:
        query["type"] = type
    if category:
        query["category"] = category
    if date:
        query["date"] = date
    data = []
    for record in records_collection.find(query).skip(skip).limit(limit):
        doc = {
            "id": str(record["_id"]),
            "title": record["title"],
            "amount": record["amount"],
            "type": record["type"],
            "category": record["category"],
            "date": record["date"],
            "notes": record["notes"],
            "created_by": record["created_by"],
            "created_at": record["created_at"]
        }
        data.append(doc)
    return {
        "page": page,
        "limit": limit,
        "data": data
    }

@app.get("/records/{record_id}")
def get_record_by_id(record_id:str, role: str = Depends(get_current_user)):
    if role not in ["admin", "analyst","viewer"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    record = records_collection.find_one({"_id":validate_object_id(record_id)})
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {
        "id" : str(record["_id"]),
        "title" : record["title"],
        "amount" : record["amount"],
        "type" : record["type"],
        "category" : record["category"],
        "date" : record["date"],
        "notes" : record["notes"],
        "created_by" : record["created_by"],
        "created_at" : record["created_at"]
    }

@app.patch("/records/{record_id}")
def update_one(record_id:str,record:RecordUpdate, role: str = Depends(get_current_user)):
    if role not in ["admin", "analyst"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = records_collection.update_one(
        {"_id": validate_object_id(record_id)},
        {"$set":record.model_dump(exclude_none=True)}    
        )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record updated"}

@app.delete("/records/{record_id}")
def delete_one(record_id:str, role: str = Depends(get_current_user)):
    if role not in ["admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = records_collection.delete_one({"_id":validate_object_id(record_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted"}



@app.get("/dashboard/summary")
def get_summary(role: str = Depends(get_current_user)):
    if role not in ["admin","analyst","viewer"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    income_pipeline = [
        {"$match":{"type":"income"}},
        {"$group":{
            "_id": None, 
            "total":{"$sum":"$amount"}
        }}
    ]
    result = list(records_collection.aggregate(income_pipeline))
    total_income = result[0]["total"] if result else 0
    expense_pipeline = [
        {"$match":{"type":"expense"}},
        {"$group":{
            "_id": None, 
            "total":{"$sum":"$amount"}
        }}
    ]
    result = list(records_collection.aggregate(expense_pipeline))
    total_expense = result[0]["total"] if result else 0
    return{
        "total_income": total_income,
        "total_expenses": total_expense,
        "net_balance": total_income-total_expense
    }

@app.get("/dashboard/category")
def get_by_category(role: str = Depends(get_current_user)):
    if role not in ["admin", "analyst", "viewer"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    pipeline = [
        {"$group": {
            "_id": "$category",        # group by category field
            "total": {"$sum": "$amount"}
        }}
    ]
    result = list(records_collection.aggregate(pipeline))
    data = {}
    for item in result:
        data[item["_id"]] = item["total"]
    return data

@app.get("/dashboard/recent")
def get_recent(role: str = Depends(get_current_user)):
    if role not in ["admin", "analyst", "viewer"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    data = []
    for record in records_collection.find().sort("created_at", -1).limit(5):
        doc = {
            "id": str(record["_id"]),
            "title": record["title"],
            "amount": record["amount"],
            "type": record["type"],
            "category": record["category"],
            "date": record["date"],
            "created_at": record["created_at"]
        }
        data.append(doc)
    return data
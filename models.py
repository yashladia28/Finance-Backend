from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

Role = Literal["viewer", "analyst", "admin"]

class UserCreate(BaseModel):
    """Used when creating a new user (incoming request body)"""
    name: str
    email: str
    password: str
    role: Role = "viewer"          # default role is viewer

class UserUpdate(BaseModel):
    """Used when updating a user — all fields optional"""
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None

class UserOut(BaseModel):
    """Used to retrieve data from the server, without passwords"""
    id:str
    name: str
    email: str
    role: Role
    is_active: bool
    created_at:datetime


#Financial Record Models
class RecordCreate(BaseModel):
    """Used when creating a new financial record"""
    title: str
    amount: float
    type: Literal["income","expense"]
    category: str
    date: str
    notes: Optional[str] = None
    created_by: str 

class RecordUpdate(BaseModel):
    """Used when updating a record — all fields optional"""
    title: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[Literal["income","expense"]] = None
    category: Optional[str] = None
    date: Optional[str] = None
    notes: Optional[str] = None

class RecordOut(BaseModel):
    """What we send back in responses"""
    id: str
    title: str
    amount: float
    type: str
    category: str
    date: str
    notes: Optional[str]
    created_by: str                # stores the user's id
    created_at: datetime
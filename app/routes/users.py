from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from app.auth.auth_handler import create_access_token
from bson import ObjectId

# Simulated in-memory database (replace with MongoDB later)
users_db = {}

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

@router.post("/signup")
async def signup(user: User):
    """
    Register a new user.
    """
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    users_db[user.username] = {"hashed_password": hashed_password}
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: User):
    """
    Authenticate a user and return a JWT token.
    """
    user_in_db = users_db.get(user.username)
    if not user_in_db or not verify_password(user.password, user_in_db["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

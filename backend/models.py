from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#this file is going to have the following

#1. Input Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str


#2. What we return to frontend
class UserResponse(BaseModel):
    email: EmailStr


#3 Functions to hash and verify passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    print("verifying password")
    return pwd_context.verify(plain_password, hashed_password)

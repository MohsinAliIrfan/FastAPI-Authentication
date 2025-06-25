from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext #this will be used for password hashing
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from pymongo import MongoClient

conn = MongoClient("")


fake_db = {
    "admin1":{
        "username": "admin1",
        "full_name": "admin",
        "email": "admin@codeupscale.com",
        "hashed_password": "",
        "disabled": False

    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): #data that will be encoded by our token
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str): #it will be  used to generate a hash for the password
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
   
    if not user:
        return False
   
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire}) #adding expiration time to the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #encpoding the data

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth_2_scheme)):

@app.post("/")
async def get_data_from_db():
    pass
    










# class Data(BaseModel):
#     name: str
#     age: int


# @app.post("/create/")
# async def create_data(data: Data):
#     return{
#         "data": data,
#     }

# @app.get("/")
# async def test():
#     return {"message": "Hello, World!"}
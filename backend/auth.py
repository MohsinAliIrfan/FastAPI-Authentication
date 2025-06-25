from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException
from backend.models import verify_password, UserCreate
from backend.database import users
from bson.objectid import ObjectId

def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # adding expiration time to the token

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # encoding the data
    print("\n ENCODED JWT:", encoded_jwt)  # Debugging line to check the encoded JWT
    return encoded_jwt


#this will handle the user login
#if the user is foundd, verifys the password and returns a jwt token
def login_user(user: UserCreate):
    
    print("logging user in")
    db_user = users.find_one({"email": user.email}) #it fetched the entire data against the email

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    #this will take the user enetered password and compare it with the hashed password in the database
    is_valid_password = verify_password(user.password, db_user["password"])

    if not is_valid_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    #now if the email and password are correct lets create a jwt token
    #we use the user_id as the identtity inside the token
    token_data = {
       "user_id": str(db_user["_id"]),
    }

    #lets set the token expire time
    access_token = create_token(
        data=token_data,
        expires_delta=timedelta(minutes=30)
    )

    # return {
    #     "access_token": access_token,
    #     "token_type": "bearer"
    # }

    return db_user
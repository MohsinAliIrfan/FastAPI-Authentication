from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Hash a password
hashed_pw = pwd_context.hash("patient")
print(hashed_pw)

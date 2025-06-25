from fastapi import APIRouter
from backend.models import UserCreate
from backend.auth import login_user

router = APIRouter()

#we would be using this when getting data through the javascript
@router.post('/login')
def login(user: UserCreate):
    return login_user(user)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils.database import get_db
from schemas import UserCreate, UserResponse
from utils.crud import create_user, get_user_by_id
from utils.auth import authenticate_user, create_access_token, get_current_user

router = APIRouter(
    prefix="/user",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    db_user = create_user(db, user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )
    return db_user

@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.phone_number})
    return {"access_token": access_token, "token_type": "bearer"}
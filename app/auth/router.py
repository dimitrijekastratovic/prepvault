from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select
from app.core.db import get_session
from app.auth.models import User
from app.auth.schemas import UserCreate, UserRead, UserLogin
from app.auth.service import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.get("/me", response_model=UserRead)
def authenticate_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/login")
def login(user: UserLogin, response: Response, session: Session = Depends(get_session)):
    user_exists = session.exec(select(User).where(User.email == user.email)).first()
    if not user_exists:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    password_correct = verify_password(user.password, user_exists.password_hash)
    if not password_correct:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    jwt_token = create_access_token({"sub": str(user_exists.id)})
    response.set_cookie(key="token", value=jwt_token, httponly=True)
    return {"message": "Login successful"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "Logout successful"}

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    user_obj = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    return user_obj

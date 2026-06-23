import bcrypt
from fastapi import HTTPException, Request, Depends
from jose import jwt
from datetime import datetime, timezone, timedelta

from sqlmodel import Session, select
from app.core.config import settings
from app.core.db import get_session
from app.auth.models import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.JWTError:
        return None

def get_user_from_token(token: str | None, session: Session) -> User | None:
    if token is None:
        return None

    payload = verify_access_token(token)
    if payload is None:
        return None

    user_id = payload.get("sub")
    return session.exec(select(User).where(User.id == user_id)).first()


def get_current_user(request: Request, session: Session = Depends(get_session)):
    user = get_user_from_token(request.cookies.get("token"), session)
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return user
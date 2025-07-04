import datetime

from passlib.context import CryptContext
from jose import jwt

from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/endpoints/user_auth/login")


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

secret_key = "sFGVBHNM,.dfrtgyhbnj"


def create_access_token(user_data: dict):
    try:
        user_data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in generating token")
    try:
        token = jwt.encode(user_data, secret_key, "HS256")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in encode")
    return token


def verify_access_token(token: str):
    try:
        user_data = jwt.decode(token, secret_key, algorithms=["HS256"])
        return user_data

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in decode")


def get_current_user(token=Depends(oauth2_schema)):
    try:
        data = verify_access_token(token)
        return data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

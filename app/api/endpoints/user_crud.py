import datetime
import os
import shutil

from fastapi import APIRouter, Form, File, UploadFile, status, Depends, HTTPException
from services.user_crud import UserCrud
from schemas.user_crud_schema import ChangeUsername, ChangePassword, ChangePhone, ChangeFullname
from core.security import get_current_user

user_crud_router = APIRouter(tags=["Todo crud"])

user_crud_service = UserCrud()


@user_crud_router.put("/api/user/change/username")
def change_username(data: ChangeUsername, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    return user_crud_service.change_username(data, user_id)


@user_crud_router.put("/api/user/change/password")
def change_password(data: ChangePassword, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    return user_crud_service.change_password(data, user_id)


@user_crud_router.put("/api/user/change/phone")
def change_phone(data: ChangePhone, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    return user_crud_service.change_phone(data, user_id)


@user_crud_router.put("/api/user/change/fullname")
def change_fullname(data: ChangeFullname, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    return user_crud_service.change_fullname(data, user_id)


@user_crud_router.put("/api/user/change/profile-image")
def change_profile_image(file: UploadFile = File(...),
                         token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    return user_crud_service.change_profile_image(user_id, file)

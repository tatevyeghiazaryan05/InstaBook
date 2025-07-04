import datetime
import os
import shutil

from fastapi import APIRouter, Form, File, UploadFile, status
from services.user_auth import UserAuth
from schemas.user_auth_schema import GenderEnum, UserSignUpSchema, VerificationCodeSchema, UserLoginSchema

user_auth_router = APIRouter(tags=["Todo auth"])

user_auth_service = UserAuth()

UPLOAD_DIR = "user_pics"


@user_auth_router.post("/api/instabook/user/sign-up",
                       status_code=status.HTTP_201_CREATED)
async def signup(
    email: str = Form(...),
    password: str = Form(...),
    fullname: str = Form(...),
    username: str = Form(...),
    phone: str = Form(...),
    birthday: datetime.date = Form(...),
    gender: GenderEnum = Form(...),
    file: UploadFile = File(None)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if file:
        ext = file.filename.split('.')[-1]
        filename = f"{username}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        profile_image = filename
    else:
        profile_image = "default_profile.png"

    user_data = UserSignUpSchema(
        email=email,
        password=password,
        fullname=fullname,
        username=username,
        phone=phone,
        birthday=birthday,
        gender=gender,
        profile_image=profile_image
    )

    return user_auth_service.signup(user_data)


@user_auth_router.post("/api/user/auth/verify")
def verify(data: VerificationCodeSchema):
    return user_auth_service.verify(data)


@user_auth_router.post("/api/user/auth/login",
                       status_code=status.HTTP_201_CREATED)
def login(data: UserLoginSchema):
    return user_auth_service.login(data)

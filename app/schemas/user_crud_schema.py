from pydantic import BaseModel, EmailStr
from enum import Enum
import datetime
from fastapi import UploadFile


class ChangeUsername(BaseModel):
    username: str


class ChangeFullname(BaseModel):
    fullname: str


class ChangePassword(BaseModel):
    password: str


class ChangePhone(BaseModel):
    phone: str


class ChangeProfileImage(BaseModel):
    pass

from pydantic import BaseModel, EmailStr
from enum import Enum
import datetime
from fastapi import UploadFile
from typing import Optional


class UpdateUserSchema(BaseModel):
    phone: Optional[str] = None
    password: Optional[str] = None
    fullname: Optional[str] = None
    username: Optional[str] = None
    image_url: Optional[str] = None

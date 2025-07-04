from pydantic import BaseModel, EmailStr
from enum import Enum
import datetime


class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class UserSignUpSchema(BaseModel):
    fullname: str
    username: str
    email: EmailStr
    password: str
    phone: str
    birthday: datetime.date
    gender: GenderEnum
    profile_image: str = "default_profile.png"


class VerificationCodeSchema(BaseModel):
    email: str
    code: str


class UserLoginSchema(BaseModel):
    login: str
    password: str

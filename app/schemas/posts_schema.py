import datetime

from pydantic import BaseModel
from typing import Optional


class CreatePostSchema(BaseModel):
    image_url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_public: Optional[bool] = True


class ChangeDescription(BaseModel):
    post_id: int
    description: str


class ChangeLocation(BaseModel):
    post_id: int
    location: str


class SavePostSchema(BaseModel):
    post_id: int


class CommentSchema(BaseModel):
    post_id: int
    comment: str


class UpdateCommentSchema(BaseModel):
    comment: str


class PostOut(BaseModel):
    description: str | None
    image_url: str
    created_at: datetime.datetime


class CommentOut(BaseModel):
    comment: str
    created_at: datetime.datetime

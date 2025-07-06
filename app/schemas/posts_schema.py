from pydantic import BaseModel
from typing import Optional


class CreatePostSchema(BaseModel):
    caption: Optional[str] = None
    location: Optional[str] = None
    is_public: Optional[bool] = True


class ChangeDescription(BaseModel):
    post_id: int
    description: str


class ChangeLocation(BaseModel):
    post_id: int
    location: str

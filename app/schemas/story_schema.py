from pydantic import BaseModel
from typing import Optional


class StorySchema(BaseModel):
    caption: Optional[str] = None
    is_video: Optional[bool] = False
    is_public: Optional[bool] = True

from pydantic import BaseModel
from typing import Optional

from enums.notification_enum import NotificationCategory


class CreateNotificationSchema(BaseModel):
    whom: int
    comment_id: Optional[int] = None
    post_id: Optional[int] = None
    category: NotificationCategory


class SavePostSchema(BaseModel):
    post_id: int


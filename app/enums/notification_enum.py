from enum import Enum


class NotificationCategory(str, Enum):
    LIKE_POST = "LIKE_POST"
    LIKE_COMMENT = "LIKE_COMMENT"
    COMMENT = "COMMENT"
    FOLLOW = "FOLLOW"

import os
import shutil
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from db_connection import DbConnection


class NotificationService:
    def __init__(self):
        self.db = DbConnection()

    def like_post(self, username: str):
        message = f"{username} liked your post "
        return message

    def like_comment(self, username: str):
        message = f"{username} liked your comment"
        return message

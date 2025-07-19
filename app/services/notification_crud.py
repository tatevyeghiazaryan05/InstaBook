import os
import shutil
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from db_connection import DbConnection


class NotificationCRUD:
    def __init__(self):
        self.db = DbConnection()

    def create_notification(self, message: str):
        try:
            self.db.cursor.execute(
                "INSERT INTO notifications (message) VALUES (%s)",
                 (message))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error creating notification")

    def get_unread_notifications(self):
        try:
            self.db.cursor.execute(
                "SELECT id, message, created_at FROM notifications WHERE is_read = %s", (False,))
            return self.db.cursor.fetchall()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error fetching notifications")

    def mark_as_read(self, notification_id: int):
        try:
            self.db.cursor.execute(
                "UPDATE notifications SET is_read = true WHERE id = %s", (notification_id,))
            self.db.conn.commit()
            return {"message": "Notification marked as read"}
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error marking as read")

    def delete_notification(self, notification_id: int):
        try:
            self.db.cursor.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error deleting notification")

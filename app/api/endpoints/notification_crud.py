from fastapi import APIRouter, Depends, HTTPException, status
from core.security import get_current_user
from services.notification_service import NotificationCRUD

notification_router = APIRouter(prefix="/adminpanel", tags=["notification_service"])
notification_service = NotificationCRUD()


@notification_service.get("/api/notifications")
def get_user_notifications(token=Depends(get_current_user)):
    return notification_service.get_unread_notifications()


@notification_service.put("/api/notifications/mark-read/{notification_id}")
def mark_notification_as_read(notification_id: int, token=Depends(get_current_user)):
    return notification_service.mark_as_read(notification_id)


@notification_service.delete("/api/admin/notifications/delete/by/id/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int, token=Depends(get_current_user)):
    notification_service.delete_notification(notification_id)


@notification_service.get("/api/notification/{notification_id}")
def get_user_notification(notification_id: int, token=Depends(get_current_user)):
    return notification_service.get_unread_notifications(notification_id)

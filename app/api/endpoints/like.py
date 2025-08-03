from fastapi import APIRouter, Depends, HTTPException, status

from schemas.posts_schema import CommentSchema, UpdateCommentSchema
from services.like import Like
from core.security import get_current_user

from services.notification_crud import NotificationCRUD
from schemas.notification_schema import CreateNotificationSchema
from enums.notification_enum import NotificationCategory


like_router = APIRouter()
like_post_service = Like()
notification_service = NotificationCRUD()


def get_post_owner(post_id: int):
    post = like_post_service.get_post_by_id(post_id)
    return post["user_id"]


@like_router.post("/api/posts/like/{post_id}")
def like_post(post_id: int, token=Depends(get_current_user)):
    try:
        who = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error"
        )

    try:
        post_owner_id = get_post_owner(post_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")

    notification_data = CreateNotificationSchema(
        whom=post_owner_id,
        category=NotificationCategory.LIKE_POST,
        post_id=post_id
    )

    notification_service.create_notification(who, notification_data)
    return like_post_service.like_post(who, post_id)


@like_router.delete("/api/posts/unlike/{post_id}")
def unlike_post(post_id: int, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")

    return like_post_service.unlike_post(user_id, post_id)


@like_router.get("/api/posts/likes-count/{post_id}")
def get_likes_count(post_id: int, token=Depends(get_current_user)):
    return like_post_service.count_likes(post_id)

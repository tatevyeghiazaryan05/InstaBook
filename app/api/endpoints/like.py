from fastapi import APIRouter, Depends, HTTPException, status

from schemas.posts_schema import CommentSchema, UpdateCommentSchema
from services.like import Like
from core.security import get_current_user

like_router = APIRouter()
like_post_service = Like()


@like_router.post("/api/posts/like/{post_id}")
def like_post(post_id: int, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")
    return like_post_service.like_post(user_id, post_id)


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

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.posts_schema import CommentSchema, UpdateCommentSchema, CommentOut
from services.comments import Comment
from core.security import get_current_user


comment_router = APIRouter()
comment_service = Comment()


@comment_router.post("/api/write/comment")
def write_comment(data: CommentSchema, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")
    return comment_service.write_comment(data, user_id)


@comment_router.get("/api/posts/comments/{post_id}",
                    response_model=List[CommentOut])
def get_comments(post_id: int, token=Depends(get_current_user)):
    return comment_service.get_comments_for_post(post_id)


@comment_router.delete("/api/delete/comment/{comment_id}")
def delete_comments(comment_id: int, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")

    return comment_service.delete_comment(comment_id, user_id)


@comment_router.put("/api/update/comment/{comment_id}")
def update_comment(comment_id: int, data: UpdateCommentSchema, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")
    return comment_service.update_comment(comment_id, user_id, data)


@comment_router.post("/api/like/comment/{comment_id}")
def like_comment(comment_id: int, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")
    return comment_service.like_comment(comment_id, user_id)


@comment_router.delete("/api/unlike/comment/{comment_id}")
def unlike_comment(comment_id: int, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")
    return comment_service.unlike_comment(comment_id, user_id)


@comment_router.get("/api/get/comment-likes/{comment_id}")
def get_comment_likes(comment_id: int, token=Depends(get_current_user)):
    return comment_service.get_comment_likes(comment_id)

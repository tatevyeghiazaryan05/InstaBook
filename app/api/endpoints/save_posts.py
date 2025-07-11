from fastapi import APIRouter, Depends, HTTPException, status

from schemas.posts_schema import SavePostSchema
from services.save_posts import SavePosts
from core.security import get_current_user

save_post_router = APIRouter()
save_post_service = SavePosts()


@save_post_router.post("/api/posts/save")
def save_post(data: SavePostSchema, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")
    return save_post_service.save_post(data, user_id)


@save_post_router.get("/api/posts/saved")
def get_saved_posts(token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")

    return save_post_service.get_saved_posts(user_id)


@save_post_router.delete("/api/posts/unsave/{post_id}")
def unsave_post(post_id: int, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")
    return save_post_service.unsave_post(post_id, user_id)

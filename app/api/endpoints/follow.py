
from fastapi import APIRouter, Depends, HTTPException, status

from services.follow import Follow
from core.security import get_current_user


follow_router = APIRouter()
follow_service = Follow()


@follow_router.post("/api/follow/user/{whom}")
def follow_to(whom: int, token=Depends(get_current_user)):
    try:
        who = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")

    return follow_service.follow(who, whom)


@follow_router.delete("/api/unfollow/{whom}")
def unfollow(whom: int,token=Depends(get_current_user)):
    try:
        who = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token error")

    return follow_service.unfollow(who, whom)



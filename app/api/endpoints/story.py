from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import FileResponse

from schemas.story_schema import StorySchema
from services.story import StoryService
from core.security import get_current_user

story_router = APIRouter(tags=["Story"])
story_service = StoryService()


@story_router.post("/api/story/upload")
def upload_story(
    caption: str = Form(None),
    is_video: bool = Form(False),
    is_public: bool = Form(True),
    file: UploadFile = File(...),
    token=Depends(get_current_user)
):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="token error")

    data = StorySchema(caption=caption, is_video=is_video, is_public=is_public)
    return story_service.create_story(3, file, data)


@story_router.delete("/api/stories/cleanup")
def cleanup_expired_stories(token=Depends(get_current_user)):
    return story_service.delete_expired_stories()


@story_router.get("/api/get/image/{image_name}")
def get_image(image_name: str):
    return FileResponse(f"./story_media/{image_name}")


@story_router.get("/api/get-story/{story_id}")
def get_story(story_id: int, token=Depends(get_current_user)):
    return story_service.get_story(story_id)


@story_router.post("/api/story/view/{story_id}")
def view_story(story_id: int, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="token error")

    return story_service.view_story(story_id, user_id)


@story_router.get("/api/story/{story_id}/viewers")
def get_viewers(story_id: int, token=Depends(get_current_user)):
    return story_service.get_story_viewers(story_id)


@story_router.get("/stories/{story_id}/views")
def get_story_views(story_id: int, token=Depends(get_current_user)):
    return story_service.get_story_view_count(story_id)

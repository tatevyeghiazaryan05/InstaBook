from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status

from typing import Optional

from schemas.posts_schema import CreatePostSchema, ChangeDescription, ChangeLocation
from services.posts_crud import PostCrud
from core.security import get_current_user

post_crud_router = APIRouter()
post_crud_service = PostCrud()


@post_crud_router.post("/api/posts/create")
def create_post(
        description: Optional[str] = Form(None),
        location: Optional[str] = Form(None),
        is_public: Optional[bool] = Form(True),
        image: UploadFile = File(...),
        token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    return post_crud_service.create_post(user_id, image, description, location, is_public)


@post_crud_router.put("/api/change/post/description")
def change_description(data: ChangeDescription, token=Depends(get_current_user)):
    return post_crud_service.change_post_description(data)


@post_crud_router.put("/api/change/post/location")
def change_description(data: ChangeLocation, token=Depends(get_current_user)):
    return post_crud_service.change_post_location(data)


@post_crud_router.delete("/api/delete/post/{post_id}")
def delete_post(post_id: int, token=Depends(get_current_user)):
    return post_crud_service.delete_post(post_id)


@post_crud_router.get("/api/get/post/{post_id}")
def get_post(post_id: int, token=Depends(get_current_user)):
    return post_crud_service.get_post(post_id)

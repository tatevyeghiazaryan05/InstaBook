import os
import shutil
import datetime

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import FileResponse

from typing import Optional

from schemas.posts_schema import CreatePostSchema, ChangeDescription, ChangeLocation , PostOut
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
    print (description)

    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_dir = os.path.join(BASE_DIR, "..", "post_images")
    os.makedirs(upload_dir, exist_ok=True)

    ext = image.filename.split(".")[-1]
    filename = f"post_{user_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    file_path = os.path.join(upload_dir, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to save image")

    image_url = f"http://localhost:8000/api/get-image/{filename}"

    data = CreatePostSchema(
        description=description,
        location=location,
        image_url=image_url,
        is_public=is_public)

    return post_crud_service.create_post(data, user_id)


@post_crud_router.get("/api/get-image/{image_name}")
def get_image(image_name: str):
    return FileResponse(f"./post_images/{image_name}")


@post_crud_router.put("/api/change/post/description")
def change_description(data: ChangeDescription, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    return post_crud_service.change_post_description(data, user_id)


@post_crud_router.put("/api/change/post/location")
def change_location(data: ChangeLocation, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    return post_crud_service.change_post_location(data, user_id)


@post_crud_router.delete("/api/delete/post/{post_id}")
def delete_post(post_id: int, token=Depends(get_current_user)):
    try:
        user_id = token.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token error")

    return post_crud_service.delete_post(post_id, user_id)


@post_crud_router.get("/api/get/post/{post_id}", response_model=PostOut)
def get_post(post_id: int, token=Depends(get_current_user)):
    return post_crud_service.get_post(post_id)

import datetime
import os
import shutil

from fastapi import APIRouter, Form, File, UploadFile, status, Depends, HTTPException
from fastapi.responses import FileResponse

from services.user_crud import UserCrud
from schemas.user_crud_schema import UpdateUserSchema
from core.security import get_current_user
user_crud_router = APIRouter(tags=["Todo crud"])

user_crud_service = UserCrud()


@user_crud_router.put("/api/users")
def user_updates(
        phone=Form(None),
        password=Form(None),
        fullname=Form(None),
        username=Form(None),
        image: UploadFile = File(None),
        token=Depends(get_current_user)):
        try:
            user_id = token.get("id")
            print(user_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token error")

        if image:

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            upload_dir = os.path.join(BASE_DIR, "user_pics")
            os.makedirs(upload_dir, exist_ok=True)

            ext = image.filename.split(".")[-1]
            filename = f"user_{user_id}_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}.{ext}"
            file_path = os.path.join(upload_dir, filename)

            try:
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
            except Exception:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Failed to save new image")

            image_url = f"http://localhost:8000/api/get_image/{filename}"
            print(image_url)
        else:
            image_url = None

        data = UpdateUserSchema(
            phone=phone,
            password=password,
            fullname=fullname,
            username=username,
            image_url=image_url
        )
        return user_crud_service.user_update(data, user_id)


@user_crud_router.get("/api/get_image/{image_name}")
def get_image(image_name: str):
    return FileResponse(f"./user_pics/{image_name}")

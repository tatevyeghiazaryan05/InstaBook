import os
from datetime import datetime, timedelta
import shutil

from fastapi import HTTPException, status, UploadFile

from db_connection import DbConnection
from schemas.user_crud_schema import ChangeUsername, ChangeFullname, ChangePassword, ChangePhone
from core.security import pwd_context
from services.email_service import send_verification_email, generate_verification_code


class UserCrud:
    def __init__(self):
        self.db = DbConnection()

    def change_username(self, data: ChangeUsername, user_id: int):
        username = data.username.strip()

        try:
            self.db.cursor.execute("""SELECT * FROM users WHERE username = %s""", (username,))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error checking for existing username")

        try:
            if self.db.cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already in use"
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching username result"
            )

        try:
            self.db.cursor.execute("""SELECT * FROM users where id=%s""",
                                   (user_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't select data")

        try:
            self.db.cursor.execute("""UPDATE users SET username = %s WHERE id = %s""",
                                   (username, user_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Can't update data")

    def change_password(self, data: ChangePassword, user_id: int):
        password = data.password.strip()
        new_hashed_password = pwd_context.hash(password)
        try:
            self.db.cursor.execute("UPDATE users SET password = %s WHERE id = %s",
                                   (new_hashed_password, user_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error updating password")

    def change_phone(self, data: ChangePhone, user_id: int):
        phone = data.phone
        try:
            self.db.cursor.execute("UPDATE users SET phone = %s WHERE id = %s",
                                   (phone, user_id))
            self.db.conn.commit()

        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error updating phone")

    def change_fullname(self, data: ChangeFullname, user_id: int):
        fullname = data.fullname
        try:
            self.db.cursor.execute("UPDATE users SET fullname = %s WHERE id = %s",
                                   (fullname, user_id))
            self.db.conn.commit()

        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error updating fullname")

    def change_profile_image(self, user_id: int, file: UploadFile):
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Only image files are allowed")

        upload_dir = os.path.join("app", "user_pics")
        os.makedirs(upload_dir, exist_ok=True)

        try:
            self.db.cursor.execute("SELECT profile_image FROM users WHERE id = %s", (user_id,))
            result = self.db.cursor.fetchone()
            print("Result fetched from DB:", result)

            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User not found")
            previous_image_url = result["profile_image"]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to fetch previous image: {e}")

        if previous_image_url and "default.jpg" not in previous_image_url:
            try:
                old_filename = previous_image_url.split("/user_pics/")[-1]
                old_path = os.path.join(upload_dir, old_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
            except Exception:
                pass

        ext = file.filename.split(".")[-1]
        filename = f"user_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        file_path = os.path.join(upload_dir, filename)

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to save new image")

        image_url = f"http://localhost:8000/user_pics/{filename}"

        try:
            self.db.cursor.execute(
                "UPDATE users SET profile_image = %s WHERE id = %s",
                (image_url, user_id)
            )
            self.db.conn.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"DB update error: {e}")

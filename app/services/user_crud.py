import os

from fastapi import HTTPException, status

from db_connection import DbConnection
from schemas.user_crud_schema import UpdateUserSchema
from core.security import pwd_context


class UserCrud:
    def __init__(self):
        self.db = DbConnection()

    def user_update(self, data: UpdateUserSchema, user_id: int):
        try:
            self.db.cursor.execute("""SELECT * FROM users WHERE id = %s""", (user_id,))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error checking for existing user")

        try:
            user = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Fetch error")

        username = data.username if data.username else user["username"]
        phone = data.phone if data.phone else user["phone"]
        fullname = data.fullname if data.fullname else user["fullname"]
        password = pwd_context.hash(data.password) if data.password else user["password"]
        image_url = data.image_url if data.image_url else user["profile_image_url"]
        print(image_url)

        try:
            if data.username == user["username"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already in use"
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching username result"
            )
        previous_image_url = dict(user)["profile_image_url"]
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        upload_dir = os.path.join(BASE_DIR, "user_pics")

        if previous_image_url and "default.jpg" not in previous_image_url:
            try:
                old_filename = previous_image_url.split("/")[-1]
                old_path = os.path.join(upload_dir, old_filename)

                if os.path.exists(old_path):
                    os.remove(old_path)

            except Exception:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't remove previous image")

        try:
            self.db.cursor.execute("""UPDATE users SET username=%s, fullname=%s, phone=%s,
                                   password=%s , profile_image_url=%s where id=%s""",
                                   (username, fullname, phone, password, image_url, user_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

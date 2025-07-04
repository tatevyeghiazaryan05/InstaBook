from datetime import datetime, timedelta

from fastapi import HTTPException, status

from db_connection import DbConnection
from schemas.user_auth_schema import UserSignUpSchema, UserLoginSchema, VerificationCodeSchema
from core.security import pwd_context
from services.email_service import send_verification_email, generate_verification_code
from core.security import create_access_token


class UserAuth:
    def __init__(self):
        self.db = DbConnection()

    def signup(self, data: UserSignUpSchema):
        username = data.username.strip()
        email = data.email.lower().strip()
        password = data.password
        fullname = data.fullname
        phone = data.phone
        birthday = data.birthday
        gender = data.gender.strip()
        profile_image = data.profile_image

        try:
            self.db.cursor.execute("""SELECT * FROM users where email=%s""",
                                   (email,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't select data")

        try:
            existing_user = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't fetch user")

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered. Please log in or use a different email.")

        self.db.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if self.db.cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username is already taken.")

        try:
            hashed_password = pwd_context.hash(password)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error hashing password")

        try:
            self.db.cursor.execute("""INSERT INTO users 
                                    (email, password, fullname, username, phone, birthday, gender, profile_image) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                                   (email, hashed_password, fullname, username,
                                    phone, birthday, gender, profile_image))
            self.db.conn.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database Query error :{e} ")

        code = generate_verification_code()

        try:
            self.db.cursor.execute("""INSERT INTO verificationcode (code, email) VALUES (%s, %s)""",
                                   (code, email))
            self.db.conn.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error inserting verification code:{e}")

        try:
            email_sent = send_verification_email(email, code)
            if not email_sent:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Failed to send verification email.")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error sending verification email")

    def verify(self, verification_data: VerificationCodeSchema):
        try:
            self.db.cursor.execute("""SELECT * FROM verificationcode 
                                WHERE email = %s AND code = %s""",
                                   (verification_data.email, verification_data.code))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database query error")

        try:
            data = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database fetch error")

        try:
            if not data:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid verification code.")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error fetching verification code")

        created_at = data['created_at']
        expiration_time = created_at + timedelta(minutes=15)
        if datetime.now() > expiration_time:
            try:
                self.db.cursor.execute("DELETE FROM verificationcode WHERE id = %s", (data.get("id"),))
                self.db.conn.commit()
            except Exception:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Error deleting expired code")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired after 15 minutes."
            )

        try:
            self.db.cursor.execute("""UPDATE users SET verified=%s WHERE email=%s""",
                                   ("true", verification_data.email))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error updating user as verified")

        try:
            self.db.cursor.execute("DELETE FROM verificationcode WHERE code= %s", (verification_data.code,))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error deleting verification code")

    def login(self, login_data: UserLoginSchema):
        login = login_data.login
        password = login_data.password

        try:
            self.db.cursor.execute("""SELECT * FROM users WHERE email = %s OR username=%s""", (login, login))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database query error")

        try:
            user = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database fetch error")

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )

        try:
            user = dict(user)
            user_password_db = user.get("password")
            user_verified = user.get("verified")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error processing user data")

        if not user_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is not verified. Please verify your email first."
            )

        if not pwd_context.verify(password, user_password_db):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password is not correct!"
            )

        try:
            user_id_db = user.get("id")
            user_email_db = user.get("email")

            token = create_access_token({"id": user_id_db, "email": user_email_db})
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Token creation error")

        return {"access_token": token}

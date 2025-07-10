from sqlalchemy import (Column, Enum, String,
                        Integer, text, TIMESTAMP,
                        Boolean, Date, ForeignKey,
                        UniqueConstraint)
import enum

from app.database import Base


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    fullname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=True)
    gender = Column(Enum(GenderEnum, name="genderenum"), nullable=True)
    verified = Column(Boolean, server_default="false")
    profile_image = Column(String, nullable=False, server_default="default_profile.png")
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class VerificationCode(Base):
    __tablename__ = "verificationcode"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)
    is_public = Column(Boolean, server_default="true")
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class SavePosts(Base):
    __tablename__ = "saveposts"

    id = Column(Integer, nullable=False, primary_key=True)

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uix_user_post"),)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

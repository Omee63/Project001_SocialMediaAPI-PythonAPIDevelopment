from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):  # Post request regulation using FastAPI. BaseModel coming from Pydantic model.
    title: str
    content: str
    published: bool = True  # if not provided, default value will be 'True'
    # rating: Optional[int] = None   # optional field. may or may not be provided. But if provided it has to be int type
    # id: Optional[int] = None


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_ad: datetime
    owner_id: int
    owner: UserOut  # A Pydantic Model which will return User according to 'UserOut' model.

    # we are telling to convert SqlAlchemy model to Pydantic model,
    # since Pydantic has no idea what to do with SqlAlchemy model
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    likes: int

    class Config:
        orm_mode = True


class UserCreation(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: str
    dir: conint(le=1)

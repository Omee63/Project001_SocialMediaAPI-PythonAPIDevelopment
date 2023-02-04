from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):  # Post request regulation using FastAPI. BaseModel coming from Pydantic model.
    title: str
    content: str
    published: bool = True  # if not provided, default value will be 'True'
    # rating: Optional[int] = None   # optional field. may or may not be provided. But if provided it has to be int type
    # id: Optional[int] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_ad: datetime

    # we are telling to convert SqlAlchemy model to Pydantic model,
    # since Pydantic has no idea what to do with SqlAlchemy model
    class Config:
        orm_mode = True


class UserCreation(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_ad: datetime

    class Config:
        orm_mode = True

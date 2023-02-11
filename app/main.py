from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import post, user, auth

models.Base.metadata.create_all(bind=engine)  # don't know actual implementation, just followed the documentation

app = FastAPI()

# class Post(BaseModel):  # Post request regulation using FastAPI. BaseModel coming from Pydantic model.
#     title: str
#     content: str
#     published: bool = True  # if not provided, default value will be 'True'
#     # optional field. may or may not be provided. But if provided it has to be int type
#     # rating: Optional[int] = None
#     # id: Optional[int] = None


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")  # @app is a decorator in py. get() is HTTP Method. "/" is root path, here its local path.
def root():
    return {"message": "Hello World!"}

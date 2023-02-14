from fastapi import FastAPI
from app import models
from app.config import settings
from app.database import engine
from app.routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


print(settings.database_username)

# This tell SqlAlchemy to run create statement so that it can generate all the tables when first started up.
# since we have Alembic we don't need below command lind
# models.Base.metadata.create_all(bind=engine)

# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]


app = FastAPI()
# we are doing below to perform CORS
app.add_middleware(
    CORSMiddleware,     # 'CORSMiddleware' is function that runs before every request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(vote.router)


@app.get("/")  # @app is a decorator in py. get() is HTTP Method. "/" is root path, here its local path.
def root():
    return {"message": "Hello World!"}

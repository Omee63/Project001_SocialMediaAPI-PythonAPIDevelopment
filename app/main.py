from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
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


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapiDB', user='postgres', password='01521504004',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfully connected to the Database!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite food",
                                                                                    "content": "I like burger",
                                                                                    "id": 2}]


def post_finder(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")  # @app is a decorator in py. get() is HTTP Method. "/" is root path, here its local path.
def root():
    return {"message": "Hello World!"}

from random import randrange
from typing import Optional
from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):  # Post request regulation using FastAPI.
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    # id: Optional[int] = None


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


@app.get("/")  # @app is a decorator in py. get() is HTTP Method. "/" is root path, here its local path.
def root():
    return {"message": "Hello World!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts",
          status_code=status.HTTP_201_CREATED)  # status code have to be selected according to HTTP response status code Documentaiton
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):  # FastAPI is Converting str ID to int ID
    post = post_finder(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    #     response.status_code = status.HTTP_404_NOT_FOUND              # hardcoded exception handler
    #     return {"message": f"Post with id: {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist.")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",  # setting prefix '/post', because every single router starts with '/post'
    tags=['Posts']
)


# Used this for testing purpose.
@router.get('/sqlalchemy', response_model=List[schemas.Post])
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# 'response_model' is the format of response from DB what we specified
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
              skip: int = 0, search: Optional[str] = ""):
    # def get_posts():
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()  # Querying to the posts according to the specific user ID
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # "select posts. *, count(votes.post_id) as likes from posts left join votes on posts.id = votes.post_id
    # group by posts.id;" we are implementing this query below.
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


# status code have to be selected according to HTTP response status code documentation
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # def create_post(post: Post):
    # # '%s' aka placeholder is representing the items of the second parameter sequentially, kind of f{} type
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(**post.dict())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # '**post.dict()' will auto unpack all the field as we needed in the previous line.
    # We do not need to type all the field.
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()  # writing this newly acquired content to the database
    db.refresh(new_post)  # retrieving back the newly added post and store back to the 'new_post'
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # def get_post(id: int, response: Response):  # FastAPI is Converting str ID to int ID
    #     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    #     post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
        filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    #     response.status_code = status.HTTP_404_NOT_FOUND              # hardcoded exception handler
    #     return {"message": f"Post with id: {id} was not found"}

    # if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # def delete_post(id: int):
    #     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    #     deleted_post = cursor.fetchone()
    #     conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # def update_post(id: int, post: Post):
    #     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                    (post.title, post.content, post.published, str(id)))
    #     updated_post = cursor.fetchone()
    #     conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # Hard coded testing
    # post_query.update({'title': 'this is my updated title', 'content': 'this is my updated content'},
    #                   synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

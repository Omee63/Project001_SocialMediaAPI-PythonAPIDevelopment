from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import database, schemas, models, utility, oauth2

router = APIRouter(tags=['Authentication'])


# 'OAuth2PasswordRequestForm' schema contains 'username' and 'password' field as a dictionary
@router.post('/login', response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utility.password_verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
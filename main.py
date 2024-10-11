from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import UserCreate, UserLogin, PostCreate, CommentCreate, LikeCreate, UserResponse, PostResponse, \
    CommentResponse, LikeResponse, CommentsListResponse, LikeCountResponse
from utils.crud import create_user, create_post, create_comment, create_like, get_post_by_id, get_comments_by_post_id, \
    get_like_count_by_post_id
from utils.auth import authenticate_user, create_access_token, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )
    return db_user


@app.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.phone_number})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/post", response_model=PostResponse)
def create_new_post(post: PostCreate, db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    db_post = create_post(db, post, current_user.id)
    return db_post


@app.post("/comment", response_model=CommentResponse)
def create_new_comment(comment: CommentCreate, post_id: int, db: Session = Depends(get_db)):
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    db_comment = create_comment(db, comment, post_id)
    return db_comment


@app.post("/like", response_model=LikeResponse)
def create_new_like(like: LikeCreate, db: Session = Depends(get_db)):
    if not get_post_by_id(db, like.post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    db_like = create_like(db, like.post_id)
    return db_like


@app.get("/post/{post_id}/comments", response_model=CommentsListResponse)
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    comments = get_comments_by_post_id(db, post_id)
    return {"comments": comments}


@app.get("/post/{post_id}/likes", response_model=LikeCountResponse)
def get_post_likes(post_id: int, db: Session = Depends(get_db)):
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    like_count = get_like_count_by_post_id(db, post_id)
    return {"count": like_count}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

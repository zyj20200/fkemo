from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.database import get_db
from schemas import CommentCreate, CommentResponse, CommentsListResponse
from utils.crud import create_comment, get_comments_by_post_id, get_comment_replies, get_post_by_id
from utils.auth import get_current_user
import models

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.post("/post/{post_id}", response_model=CommentResponse)
def create_new_comment(comment: CommentCreate, post_id: int, db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    db_comment = create_comment(db, comment, post_id, current_user)
    return db_comment


@router.get("/post/{post_id}", response_model=CommentsListResponse)
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    comments = get_comments_by_post_id(db, post_id)
    for comment in comments:
        comment.replies = get_comment_replies(db, comment.id)
    return {"comments": comments}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from utils.database import get_db
from schemas import CommentCreate, CommentResponse, CommentsListResponse
from utils.crud import create_comment, get_comments_by_post_id, get_post_by_id

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/post/{post_id}", response_model=CommentResponse)
def create_new_comment(comment: CommentCreate, post_id: int, db: Session = Depends(get_db)):
    """发表评论"""
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    db_comment = create_comment(db, comment, post_id)
    return db_comment

@router.get("/post/{post_id}", response_model=CommentsListResponse)
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    """获取某个帖子的所有评论"""
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    comments = get_comments_by_post_id(db, post_id)
    return {"comments": comments}
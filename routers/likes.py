from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.database import get_db
from schemas import LikeCreate, LikeActionResponse, LikeCountResponse
from utils.crud import toggle_like, get_post_by_id, get_like_count_by_post_id
from utils.auth import get_current_user
import models

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
    responses={404: {"description": "Not found"}},
)

@router.post("/post/{post_id}", response_model=LikeActionResponse)
def toggle_like_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    result = toggle_like(db, post_id, current_user)
    return result

@router.get("/post/{post_id}/count", response_model=LikeCountResponse)
def get_post_likes(post_id: int, db: Session = Depends(get_db)):
    """获取帖子的点赞数"""
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    like_count = get_like_count_by_post_id(db, post_id)
    return {"count": like_count}
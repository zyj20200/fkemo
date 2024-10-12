from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.database import get_db
from schemas import LikeResponse, LikeCountResponse # ,LikeCreate
from utils.crud import create_like, get_post_by_id, get_like_count_by_post_id

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
    responses={404: {"description": "Not found"}},
)

@router.post("/post/{post_id}", response_model=LikeResponse)
def create_new_like(post_id: int, db: Session = Depends(get_db)):
    """点赞帖子"""
    if not get_post_by_id(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    db_like = create_like(db, post_id)
    return db_like

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
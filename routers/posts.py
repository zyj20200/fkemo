from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from utils.database import get_db
from schemas import PostCreate, PostResponse, PagedPostResponse
from utils.crud import create_post, get_user_post_count, get_user_posts, get_following_users_post_count, \
    get_following_users_posts, get_specific_following_user_post_count, get_specific_following_user_posts
from utils.auth import get_current_user
import models

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=PostResponse)
def create_new_post(post: PostCreate, db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    """创建新帖子"""
    db_post = create_post(db, post, current_user.id)
    return db_post


@router.get("/me", response_model=PagedPostResponse)
def get_my_posts(page: int = 1, page_size: int = 10, current_user: models.User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    """获取当前用户的所有帖子并分页显示"""
    skip = (page - 1) * page_size
    total = get_user_post_count(db, current_user.id)
    posts = get_user_posts(db, current_user.id, skip=skip, limit=page_size)
    return {"total": total, "posts": posts}


@router.get("/me/following", response_model=PagedPostResponse)
def get_following_posts(page: int = 1, page_size: int = 10, current_user: models.User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """获取当前用户的关注用户的所有帖子并分页显示"""
    skip = (page - 1) * page_size
    total = get_following_users_post_count(db, current_user.id)
    posts = get_following_users_posts(db, current_user.id, skip=skip, limit=page_size)
    return {"total": total, "posts": posts}


@router.get("/me/following/{following_id}", response_model=PagedPostResponse)
def get_specific_user_posts(following_id: int, page: int = 1, page_size: int = 10,
                            current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取关注用户的某个用户的所有帖子并分页显示"""
    skip = (page - 1) * page_size
    total = get_specific_following_user_post_count(db, current_user.id, following_id)
    if total is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not following this user",
        )
    posts = get_specific_following_user_posts(db, current_user.id, following_id, skip=skip, limit=page_size)
    return {"total": total, "posts": posts}

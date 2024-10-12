from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.database import get_db
from schemas import FollowCreate, FollowResponse, FollowingListResponse, FollowersListResponse, FollowedUser
from utils.crud import create_follow, get_user_by_id, get_following_users, get_follower_users
from utils.auth import get_current_user
import models
router = APIRouter(
    prefix="/follows",
    tags=["follows"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=FollowResponse)
def follow_user(follow: FollowCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """关注用户 """
    if not get_user_by_id(db, follow.following_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db_follow = create_follow(db, current_user.id, follow.following_id)
    if db_follow is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already following this user",
        )
    return db_follow

@router.get("/me/following", response_model=FollowingListResponse)
def get_following(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取关注的用户列表"""
    followed = get_following_users(db, current_user.id)
    result = []
    for f in followed:
        user = get_user_by_id(db, f.following_id)
        result.append(user)
    return {"following": result, "count": len(result)}

@router.get("/me/followers", response_model=FollowersListResponse)
def get_followers(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取粉丝列表"""
    followers = get_follower_users(db, current_user.id)
    result = []
    for f in followers:
        user = get_user_by_id(db, f.follower_id)
        result.append(user)
    return {"followers": result, "count": len(result)}
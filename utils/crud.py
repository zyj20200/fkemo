from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, Post, Comment, Like, Follow
from schemas import UserCreate, PostCreate, CommentCreate, LikeCreate, FollowCreate
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_phone(db: Session, phone_number: str):
    return db.query(User).filter(User.phone_number == phone_number).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(phone_number=user.phone_number, hashed_password=hashed_password, nickname=user.nickname)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        return None
    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(content=post.content, user_id=user_id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def create_comment(db: Session, comment: CommentCreate, post_id: int):
    db_comment = Comment(content=comment.content, post_id=post_id, nickname=comment.nickname,
                         created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def create_like(db: Session, post_id: int):
    db_like = Like(post_id=post_id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def get_comments_by_post_id(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at).all()


def get_like_count_by_post_id(db: Session, post_id: int):
    return db.query(Like).filter(Like.post_id == post_id).count()


def create_follow(db: Session, follower_id: int, following_id: int):
    db_follow = Follow(follower_id=follower_id, following_id=following_id)
    db.add(db_follow)
    try:
        db.commit()
        db.refresh(db_follow)
    except IntegrityError:
        db.rollback()
        return None
    return db_follow


def get_following_users(db: Session, user_id: int):
    return db.query(Follow).filter(Follow.follower_id == user_id).all()

def get_follower_users(db: Session, user_id: int):
    return db.query(Follow).filter(Follow.following_id == user_id).all()
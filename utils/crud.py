from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, Post, Comment, Like
from schemas import UserCreate, PostCreate, CommentCreate, LikeCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_phone(db: Session, phone_number: str):
    return db.query(User).filter(User.phone_number == phone_number).first()


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
    db_post = Post(content=post.content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def create_comment(db: Session, comment: CommentCreate, post_id: int):
    db_comment = Comment(content=comment.content, post_id=post_id, nickname=comment.nickname)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def create_like(db: Session, post_id: int):
    db_like = Like(post_id=post_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def get_comments_by_post_id(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at).all()


def get_like_count_by_post_id(db: Session, post_id: int):
    return db.query(Like).filter(Like.post_id == post_id).count()

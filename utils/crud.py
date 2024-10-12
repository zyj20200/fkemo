from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, Post, Comment, Like, Follow, InterestCategory, FanType
from schemas import UserCreate, PostCreate, CommentCreate, FollowCreate, InterestCategoryCreate, \
    FanTypeCreate
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_phone(db: Session, phone_number: str):
    return db.query(User).filter(User.phone_number == phone_number).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    interest_categories = ",".join(user.interest_categories) if user.interest_categories else ""
    fan_types = ",".join(user.fan_types) if user.fan_types else ""
    db_user = User(
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        nickname=user.nickname,
        role=user.role,
        interest_categories=interest_categories,
        fan_types=fan_types
    )
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


def create_comment(db: Session, comment: CommentCreate, post_id: int, current_user: User):
    db_comment = Comment(content=comment.content, post_id=post_id, nickname=current_user.nickname,
                         created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def toggle_like(db: Session, post_id: int, current_user: User):
    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == current_user.id).first()
    if like:
        if like.is_deleted:
            like.is_deleted = False
            like.updated_at = datetime.utcnow()
            db.commit()
            return {"action": "liked", "like": like}
        else:
            like.is_deleted = True
            like.updated_at = datetime.utcnow()
            db.commit()
            return {"action": "unliked"}
    else:
        db_like = Like(post_id=post_id, user_id=current_user.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), is_deleted=False)
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return {"action": "liked", "like": db_like}

def get_like_count_by_post_id(db: Session, post_id: int):
    return db.query(Like).filter(Like.post_id == post_id, Like.is_deleted == False).count()


def get_comments_by_post_id(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at).all()



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


def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Post).filter(Post.user_id == user_id).order_by(Post.created_at.desc()).offset(skip).limit(
        limit).all()


def get_following_users_posts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    following_ids = db.query(Follow.following_id).filter(Follow.follower_id == user_id).subquery()
    return db.query(Post).filter(Post.user_id.in_(following_ids)).order_by(Post.created_at.desc()).offset(skip).limit(
        limit).all()


def get_user_post_count(db: Session, user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).count()


def get_following_users_post_count(db: Session, user_id: int):
    following_ids = db.query(Follow.following_id).filter(Follow.follower_id == user_id).subquery()
    return db.query(Post).filter(Post.user_id.in_(following_ids)).count()


def get_specific_following_user_posts(db: Session, follower_id: int, following_id: int, skip: int = 0, limit: int = 10):
    # 检查当前用户是否关注了该用户
    follow_relation = db.query(Follow).filter(Follow.follower_id == follower_id,
                                              Follow.following_id == following_id).first()
    if follow_relation:
        return db.query(Post).filter(Post.user_id == following_id).order_by(Post.created_at.desc()).offset(skip).limit(
            limit).all()
    else:
        return None


def get_specific_following_user_post_count(db: Session, follower_id: int, following_id: int):
    # 检查当前用户是否关注了该用户
    follow_relation = db.query(Follow).filter(Follow.follower_id == follower_id,
                                              Follow.following_id == following_id).first()
    if follow_relation:
        return db.query(Post).filter(Post.user_id == following_id).count()
    else:
        return None


def create_interest_category(db: Session, category: InterestCategoryCreate):
    db_category = InterestCategory(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_all_interest_categories(db: Session):
    return db.query(InterestCategory).all()


def create_fan_type(db: Session, fan_type: FanTypeCreate):
    db_fan_type = FanType(name=fan_type.name)
    db.add(db_fan_type)
    db.commit()
    db.refresh(db_fan_type)
    return db_fan_type


def get_all_fan_types(db: Session):
    return db.query(FanType).all()

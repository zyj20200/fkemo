from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    phone_number: str
    password: str
    nickname: str

class UserLogin(BaseModel):
    phone_number: str
    password: str

class UserResponse(BaseModel):
    id: int
    phone_number: str
    nickname: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    content: str

class PostResponse(BaseModel):
    id: int
    content: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str
    nickname: str = None

class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    nickname: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LikeCreate(BaseModel):
    post_id: int

class LikeResponse(BaseModel):
    id: int
    post_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommentsListResponse(BaseModel):
    comments: List[CommentResponse]

    class Config:
        from_attributes = True

class LikeCountResponse(BaseModel):
    count: int

    class Config:
        from_attributes = True
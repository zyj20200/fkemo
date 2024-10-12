from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional


class UserCreate(BaseModel):
    phone_number: str
    password: str
    nickname: str
    role: str = "user"
    interest_categories: Optional[List[str]] = []
    fan_types: Optional[List[str]] = []


class UserLogin(BaseModel):
    phone_number: str
    password: str


class UserResponse(BaseModel):
    id: int
    phone_number: str
    nickname: str
    role: str
    created_at: datetime
    updated_at: datetime
    interest_categories: List[str] = []
    fan_types: List[str] = []

    @field_validator('interest_categories', mode='before')
    def handle_interest_categories(cls, value):
        if isinstance(value, str):
            return value.split(",")
        return value

    @field_validator('fan_types', mode='before')
    def handle_fan_types(cls, value):
        if isinstance(value, str):
            return value.split(",")
        return value

    class Config:
        orm_mode = True


class PostImageResponse(BaseModel):
    id: int
    image_url: str

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    content: str


class PostResponse(BaseModel):
    id: int
    content: str
    images: List[PostImageResponse] = Field(default_factory=list)
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PagedPostResponse(BaseModel):
    total: int
    posts: List[PostResponse]

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int
    nickname: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LikeCreate(BaseModel):
    post_id: int


class LikeResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LikeActionResponse(BaseModel):
    action: str
    like: Optional[LikeResponse] = None

    class Config:
        orm_mode = True


class FollowCreate(BaseModel):
    following_id: int


class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CommentsListResponse(BaseModel):
    comments: List[CommentResponse]

    class Config:
        orm_mode = True


class LikeCountResponse(BaseModel):
    count: int

    class Config:
        orm_mode = True


class FollowedUser(BaseModel):
    id: int
    phone_number: str
    nickname: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FollowingListResponse(BaseModel):
    following: List[FollowedUser]
    count: int

    class Config:
        orm_mode = True


class FollowersListResponse(BaseModel):
    followers: List[FollowedUser]
    count: int

    class Config:
        orm_mode = True


class InterestCategoryCreate(BaseModel):
    name: str


class InterestCategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class FanTypeCreate(BaseModel):
    name: str


class FanTypeResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True

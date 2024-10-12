import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import engine
import models
from routers import users, posts, comments, likes, follows, categories, fan_types

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的请求源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(fan_types.router)
app.include_router(follows.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

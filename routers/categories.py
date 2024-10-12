from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from schemas import InterestCategoryCreate, InterestCategoryResponse
from utils.crud import create_interest_category, get_all_interest_categories
from typing import List

router = APIRouter(
    prefix="/interest_categories",
    tags=["interest_categories"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[InterestCategoryResponse])
def get_interest_categories(db: Session = Depends(get_db)):
    categories = get_all_interest_categories(db)
    return categories

@router.post("/", response_model=InterestCategoryResponse)
def create_interest_categories(category: InterestCategoryCreate, db: Session = Depends(get_db)):
    db_category = create_interest_category(db, category)
    return db_category
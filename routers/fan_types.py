from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from schemas import FanTypeCreate, FanTypeResponse
from utils.crud import create_fan_type, get_all_fan_types
from typing import List

router = APIRouter(
    prefix="/fan_types",
    tags=["fan_types"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[FanTypeResponse])
def get_fan_types(db: Session = Depends(get_db)):
    fan_types = get_all_fan_types(db)
    return fan_types

@router.post("/", response_model=FanTypeResponse)
def create_fan_types(fan_type: FanTypeCreate, db: Session = Depends(get_db)):
    db_fan_type = create_fan_type(db, fan_type)
    return db_fan_type
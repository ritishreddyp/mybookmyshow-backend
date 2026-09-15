from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.api.deps import require_role
from app.schemas.admin import MainAdminProvisionCreate
from app.schemas.theater_admin import TheaterAdminCreate
from app.curd_operations.admin_operations import create_main_admin_account,create_theater_admin_account

router = APIRouter()

@router.post("/main-admin", status_code=status.HTTP_201_CREATED)
def create_main_admin(payload: MainAdminProvisionCreate, db: Session = Depends(get_db),current_user = Depends(require_role(["admin"]))):
    return create_main_admin_account(payload, db)

@router.post("/theater-admin")
def create_theater_admin(payload: TheaterAdminCreate, db: Session = Depends(get_db), current_user = Depends(require_role(["admin"]))):
    return create_theater_admin_account(payload, db)
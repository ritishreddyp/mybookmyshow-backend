from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.db import get_db
from app.api.deps import require_role

from app.curd_operations.user import create_new_user,update_user_details,delete_user,get_all_users,get_user_id
from app.schemas.user import UserCreate, UserUpdate,UserDetails

router = APIRouter()

# user access
@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(user, db)

# admin access 
@router.get("/")
def get_users(db:Session =Depends(get_db), current_user = Depends(require_role(["admin"]))):
    return get_all_users(db)

@router.delete("/{user_id}")
def remove_user(user_id:UUID ,db: Session = Depends(get_db), current_user = Depends(require_role(["admin","public"]))):
    return delete_user(user_id, db)

# user - admin access
@router.get("/{user_id}")
def get_user_by_id(user_id:UUID,db:Session = Depends(get_db), current_user = Depends(require_role(["public", "admin"]))):
    return get_user_id(user_id,db)

@router.patch("/{user_id}")
def update_user(user_id: UUID,user: UserUpdate,db: Session = Depends(get_db), current_user = Depends(require_role(["public", "admin"]))):
    return update_user_details(user_id, user, db)
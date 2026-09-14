from fastapi import  APIRouter,Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.api.deps import require_role

from app.schemas.shows import ShowCreate, ShowUpdate
from app.curd_operations.shows import create_show, update_show, delete_show, get_shows

router = APIRouter()

# public access
@router.get("/")
def list_shows( city_id: int | None = None,theater_id: int | None = None, screen_id: int | None = None, movie_id: int | None = None, language_id: int | None = None, db: Session = Depends(get_db)):
    return get_shows( city_id=city_id,  theater_id=theater_id,  local_screen_id=screen_id, movie_id=movie_id, language_id=language_id,  db=db  )


# theater admin 
@router.post("/")
def schedule_show(show: ShowCreate, db: Session = Depends(require_role(["theater_admin", "admin"]))):
    return create_show(show, db)

@router.patch("/{show_id}")
def modify_show(show_id: int, show_update: ShowUpdate, db: Session = Depends(require_role(["theater_admin", "admin"]))):
    return update_show(show_id, show_update, db)

@router.delete("/{show_id}")
def remove_show(show_id: int, db: Session = Depends(require_role(["theater_admin", "admin"]))):
    return delete_show(show_id, db)




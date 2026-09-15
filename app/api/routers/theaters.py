from fastapi import APIRouter, Depends,status,Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.api.deps import require_role
from app.models.user import SQUser
from app.schemas.theatres import TheatreCreate,TheatreDetails,TheatreUpdate
from app.curd_operations.theater import get_all_theaters,get_theater_by_id,update_theater,delete_theater,get_inactive_theaters,create_new_theater

from app.schemas.screens import ScreenCreate, ScreenDetails, ScreenUpdate
from app.curd_operations.screen import add_screen_to_theater, get_screens_by_theater,update_screen,delete_screen,get_inactive_screens_by_theater,activate_screen
from app.schemas.theater_admin import TheaterAdminCreate
from app.curd_operations.admin_operations import create_theater_admin_account

router = APIRouter()

# public access
@router.get("/")
def list_theaters(city_id: UUID | None = Query(None, description="Filter theaters by city ID"), db: Session = Depends(get_db)):
    return get_all_theaters(city_id, db)

# admin
@router.get("/admin/inactive")
def list_inactive_theaters(db: Session =Depends(get_db), current_user: SQUser = Depends(require_role(["admin"]))):
    return get_inactive_theaters(db)

#public
@router.get("/{theater_id}")
def get_single_theater(theater_id: UUID, db: Session = Depends(get_db)):
    return get_theater_by_id(theater_id, db)


#admin
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_theater(payload: TheatreCreate, db: Session = Depends(get_db), current_user: SQUser = Depends(require_role(["admin"]))):
    return create_new_theater(payload, db)

@router.put("/{theater_id}")
def edit_theater(theater_id: UUID, theater: TheatreUpdate, db: Session = Depends(get_db), current_user: SQUser =Depends(require_role(["admin"]))):
    return update_theater(theater_id, theater, db)

@router.delete("/{theater_id}")
def remove_theater(theater_id: UUID, db: Session =Depends(get_db), current_user: SQUser = Depends(require_role(["admin"]))):
    return delete_theater(theater_id, db)




# theater admin
#screens
@router.get("/{theater_id}/screens/")
def list_theater_screens(theater_id: UUID, db: Session =Depends(get_db), current_user: SQUser = Depends(require_role(["theater_admin", "admin"]))):
    return get_screens_by_theater(theater_id, db)

@router.post("/{theater_id}/screens/")
def add_screen(theater_id: UUID, screen_name: str, screen_type: str, db: Session =Depends(get_db), current_user: SQUser = Depends(require_role(["theater_admin", "admin"]))):
    return add_screen_to_theater(theater_id, screen_name, screen_type, db)

@router.put("/screens/{screen_id}")
def edit_screen(screen_id: UUID, screen: ScreenUpdate, db: Session =Depends(get_db), current_user: SQUser = Depends(require_role(["theater_admin", "admin"]))):
    return update_screen(screen_id, screen, db)

@router.delete("/screens/{screen_id}")
def remove_screen(screen_id: UUID, db: Session =Depends(get_db), current_user: SQUser = Depends(require_role(["theater_admin", "admin"]))):
    return delete_screen(screen_id, db)

@router.get("/theaters/{theater_id}/screens/inactive")
def list_inactive_theater_screens(theater_id: UUID, db: Session =Depends(get_db), current_user: SQUser = Depends(require_role(["theater_admin", "admin"]))):
    return get_inactive_screens_by_theater(theater_id, db)

@router.patch("/{screen_id}/activate")
def restore_screen(screen_id: UUID, db: Session =Depends(get_db), current_user: SQUser = Depends(require_role(["theater_admin", "admin"]))):
    return activate_screen(screen_id, db)

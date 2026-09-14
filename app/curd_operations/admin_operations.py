import re
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash

from app.models.admin import SQMainAdmin
from app.models.theater_admin import SQTheaterAdmin
from app.models.theaters import SQtheaters

#main admin
def create_main_admin_account(payload, db: Session):
    email = payload.email.lower().strip()
    if not re.match(r"^[a-z0-9._%+-]+\.admin@mybookmyshow\.com$", email):
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid admin mail format" )

    if db.query(SQMainAdmin).count() >= 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Maximum limit of 10 main admins reached.")
    
    if db.query(SQMainAdmin).filter(SQMainAdmin.email == email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Main admin already exists.")
    
    new_admin = SQMainAdmin(email=email, hashed_password=get_password_hash(payload.password))
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin

# theater admin
def create_theater_admin_account(payload, db: Session):
    theater = db.query(SQtheaters).filter(
        SQtheaters.city_id == payload.city_id,
        SQtheaters.theater_id == payload.theater_id
    ).first()

    if not theater:
        raise HTTPException(status_code=404, detail="Theater not found for given city_id and theater_id")

    hashed_pw = get_password_hash(payload.admin_password)

    new_admin = SQTheaterAdmin(
        city_id=payload.city_id,
        theater_id=payload.theater_id,
        theater_name=theater.theater_name,
        email=payload.admin_username,
        hashed_password=hashed_pw
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin
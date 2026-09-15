from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token

from app.models.user import SQUser
from app.models.admin import SQMainAdmin
from app.models.theater_admin import SQTheaterAdmin

#user authentication 
def authenticate_customer(email: str, password: str, db: Session):

    email = email.lower().strip()
    user = db.query(SQUser).filter(SQUser.email == email).first()
    hashed_pw = getattr(user, "hashed_password", getattr(user, "password", ""))
    if not user or not verify_password(password, hashed_pw):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials")
    
    access_token = create_access_token(email=user.email, role="user", theater_id=None)

    return {"access_token": access_token, "token_type": "bearer"}

# admin authentication 
def authenticate_main_admin(email: str, password: str, db: Session):

    email = email.lower().strip()
    admin = db.query(SQMainAdmin).filter(SQMainAdmin.email == email).first()
    hashed_pw = getattr(admin, "hashed_password", getattr(admin, "password", ""))
    if not admin or not verify_password(password, hashed_pw):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")
    
    access_token = create_access_token(email=admin.email, role="admin", theater_id=None)

    return {"access_token": access_token, "token_type": "bearer"}


# theater admin authentication 
def authenticate_theater_admin(email: str, password: str, db: Session):

    email = email.lower().strip()
    t_admin = db.query(SQTheaterAdmin).filter(SQTheaterAdmin.email == email).first()
    hashed_pw = getattr(t_admin, "hashed_password", getattr(t_admin, "password", ""))
    if not t_admin or not verify_password(password, hashed_pw):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid theater admin credentials")
    
    access_token = create_access_token(email=t_admin.email, role="theater_admin", theater_id=t_admin.theater_id)
    
    return {"access_token": access_token, "token_type": "bearer"}
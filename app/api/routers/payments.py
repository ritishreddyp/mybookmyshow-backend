from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.api.deps import require_role
from uuid import UUID

from app.models.user import SQUser
from app.schemas.payments import PaymentProcessRequest
from app.schemas.tickets import BookingConfirmation
from app.curd_operations.payment import get_checkout_summary,get_payment_methods,initiate_payment,verify_and_confirm_payment,select_payment_method


router = APIRouter()

# public access
@router.get("/checkout/{booking_id}")
def get_checkout(booking_id: UUID , db: Session = Depends(get_db),  current_user: SQUser = Depends(require_role(["user", "admin"]))):
    return get_checkout_summary(booking_id=booking_id, user_id=current_user.id, db=db)


@router.get("/methods")
def list_methods():
    return get_payment_methods()

@router.get("/methods/{category_id}")
def select_method(category_id: str):
    return select_payment_method(category_id=category_id)


@router.post("/initiate")
def initiate_txn(payload: PaymentProcessRequest, db: Session = Depends(get_db), current_user: SQUser = Depends(require_role(["admin","user"]))):
    return initiate_payment(payload=payload, user_id=current_user.id, db=db)


@router.post("/verify")
def verify_txn( booking_id: UUID , transaction_id: str,  db: Session = Depends(get_db), current_user: SQUser = Depends(require_role(["admin","user"]))):
    return verify_and_confirm_payment(booking_id=booking_id, transaction_id=transaction_id, user_id=current_user.id, db=db)
    
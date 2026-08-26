from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.payments import PaymentProcessRequest
from app.schemas.tickets import BookingConfirmation
from app.crud import get_checkout_summary,get_payment_methods,initiate_payment,verify_and_confirm_payment,select_payment_method


router = APIRouter()


@router.get("/checkout/{booking_id}", status_code=status.HTTP_200_OK)
def get_checkout(booking_id: int, db: Session = Depends(get_db)):
    current_user_id = 1
    return get_checkout_summary(booking_id=booking_id, user_id=current_user_id, db=db)


@router.get("/methods", status_code=status.HTTP_200_OK)
def list_methods():
    return get_payment_methods()

@router.get("/methods/{category_id}", status_code=status.HTTP_200_OK)
def select_method(category_id: str):
    return select_payment_method(category_id=category_id)


@router.post("/initiate", status_code=status.HTTP_201_CREATED)
def initiate_txn(payload: PaymentProcessRequest, db: Session = Depends(get_db)):
    current_user_id = 1
    return initiate_payment(payload=payload, user_id=current_user_id, db=db)


@router.post("/verify", response_model=BookingConfirmation, status_code=status.HTTP_200_OK)
def verify_txn(booking_id: int, transaction_id: str, db: Session = Depends(get_db)):
    current_user_id = 1
    return verify_and_confirm_payment(booking_id=booking_id, transaction_id=transaction_id, user_id=current_user_id, db=db)
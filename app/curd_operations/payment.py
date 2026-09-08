from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.models.payments import SQpayments
from app.schemas.payments import PaymentProcessRequest

from app.models.booking_section import SQbooking_section
from app.models.booking_item import SQbooking_items
from app.models.show_seats import SQshow_seats
from app.models.tickets import SQtickets
# ================================================= payments =============================================================

# To ger all user bookings
def get_user_booking(booking_id: int, user_id: int, db: Session):
    booking = db.query(SQbooking_section).filter_by(booking_id=booking_id, user_id=user_id).first()
    if not booking:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Booking not found.")
    
    return booking


# payment checkout
def get_checkout_summary(booking_id: int, user_id: int, db: Session):

    booking = get_user_booking(booking_id, user_id, db)
    items = db.query(SQbooking_items).filter_by(booking_id=booking_id).all()
    seats = db.query(SQshow_seats).filter(SQshow_seats.show_seat_id.in_([i.show_seat_id for i in items])).all()

    if any(s.lock_expires_at and s.lock_expires_at < datetime.now() for s in seats):
        for s in seats: s.status, s.lock_expires_at = "available", None
        booking.booking_status = "Expired"

        db.commit()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Checkout session expired.")

    ticket_price = sum(i.price for i in items)
    convenience_fees = round(ticket_price * 0.1015, 2), 2.0
    booking.total_amount = round(ticket_price + convenience_fees , 2)

    db.commit()
    return {
        "booking_id": booking.booking_id, "show_id": booking.show_id, "booking_status": booking.booking_status,
        "pricing_breakdown": {"ticket_price": ticket_price, "convenience_fees": convenience_fees, "order_total": booking.total_amount},
        "seats_count": len(items), "lock_expires_at": seats[0].lock_expires_at if seats else None}


# payment methods
PAYMENT_CATEGORIES = {
    "upi": {
        "id": "upi",
        "name": "Pay by any UPI App",
        "options": ["Scan QR Code", "GPay", "PhonePe", "Paytm"]
    },
    "cards": {
        "id": "cards",
        "name": "Debit/Credit Card",
        "options": ["Visa", "Mastercard", "RuPay"]
    },
    "wallets": {
        "id": "wallets",
        "name": "Mobile Wallets",
        "options": ["Paytm", "Amazon Pay", "Mobikwik"]
    },
    "net_banking": {
        "id": "net_banking",
        "name": "Net Banking",
        "options": ["HDFC", "ICICI", "SBI", "Axis"]
    },
    "pay_later": {
        "id": "pay_later",
        "name": "Pay Later",
        "options": ["Simpl", "LazyPay"]
    }
}


# to view methods
def get_payment_methods():
    return {"payment_categories": list(PAYMENT_CATEGORIES.values())}


# to select method
def select_payment_method(category_id: str):
    category = PAYMENT_CATEGORIES.get(category_id.strip().lower())
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment method '{category_id}' not found. Available options: {list(PAYMENT_CATEGORIES.keys())}" )
    return {
        "message": f"Payment method '{category['name']}' selected successfully.",
        "selected_category": category,
        "next_step": "Proceed to POST /payments/initiate with booking_id and payment_method"
    }


#payment intiation
def initiate_payment(payload: PaymentProcessRequest, user_id: int, db: Session):
    booking = get_user_booking(payload.booking_id, user_id, db)
    if booking.booking_status != "Pending":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Booking is not pending.")

    txn_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
    payment = SQpayments(booking_id=booking.booking_id, transaction_id=txn_id, payment_method=payload.payment_method, amount=booking.total_amount, payment_status="Processing")

    db.add(payment)
    db.commit()

    return {
        "payment_id": payment.payment_id, "booking_id": booking.booking_id, "transaction_id": txn_id,
        "payable_amount": payment.amount, "payment_status": payment.payment_status,
        "upi_qr_payload": f"upi://pay?pa=bookmyshow@icici&pn=BookMyShow&am={booking.total_amount}&tr={txn_id}&cu=INR" if payload.payment_method.upper() == "UPI" else None}


#  confirm booking
def verify_and_confirm_payment(booking_id: int, transaction_id: str, user_id: int, db: Session):

    booking = get_user_booking(booking_id, user_id, db)
    payment = db.query(SQpayments).filter_by(booking_id=booking_id, transaction_id=transaction_id).first()
    if not payment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Payment transaction not found.")

    items = db.query(SQbooking_items).filter_by(booking_id=booking_id).all()
    seats = db.query(SQshow_seats).filter(SQshow_seats.show_seat_id.in_([i.show_seat_id for i in items])).all()
    if any(s.lock_expires_at and s.lock_expires_at < datetime.now() for s in seats):

        payment.payment_status, booking.booking_status = "Failed", "Expired"
        for s in seats: s.status, s.lock_expires_at = "available", None

        db.commit()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Payment failed: Lock timer expired.")


    for seat in seats:
        seat.status = "booked"
        seat.lock_expires_at = None

    payment.payment_status, booking.booking_status = "Success", "Confirmed"
    ticket = SQtickets(booking_id=booking.booking_id, show_id=booking.show_id, ticket_code=f"BMS-TKT-{uuid.uuid4().hex[:8].upper()}", ticket_status="Confirmed")

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    db.refresh(payment)

    return {"booking_id": booking.booking_id, "total_amount": booking.total_amount, "booking_status": booking.booking_status, "ticket": ticket, "payment": payment}


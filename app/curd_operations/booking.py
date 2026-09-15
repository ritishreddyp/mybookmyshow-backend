from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import UUID
from app.models.booking_section import SQbooking_section
from app.models.booking_item import SQbooking_items

from app.models.shows import SQshows
from app.models.show_seats import SQshow_seats

#---------------------------------------------------------- Booking operations ---------------------------------------------------------#

# Select show seats  
def select_seats_and_create_summary(booking_data, current_user_id, db):

    show = db.query(SQshows).filter(SQshows.show_id == booking_data.show_id).first()
    if not show:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Show not found")
    
    seats = db.query(SQshow_seats).filter(SQshow_seats.show_id == booking_data.show_id,SQshow_seats.show_seat_id.in_(booking_data.show_seat_id)).all()
    if len(seats) != len(booking_data.show_seat_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="One or more selected seats are invalid for this show.")

    for seat in seats:
        if seat.status != "available":
            raise HTTPException(status.HTTP_400_BAD_REQUEST,   detail=f"Seat ID {seat.show_seat_id} is currently {seat.status} and cannot be selected.")

    lock_expiration_time = datetime.now() + timedelta(minutes=10)

    for seat in seats:
        seat.status = "locked"
        seat.lock_expires_at = lock_expiration_time

    new_booking = SQbooking_section(user_id=current_user_id, show_id=booking_data.show_id,booking_status="Pending",total_amount=sum(seat.price for seat in seats))

    db.add(new_booking)
    db.flush() 

    booking_items = []

    for seat in seats:
        item = SQbooking_items(booking_id=new_booking.booking_id,show_seat_id=seat.show_seat_id,price=seat.price )
        db.add(item)
        booking_items.append(item)

    db.commit()
    db.refresh(new_booking)
    
    return {
        "message": "Order summary created successfully! Seats are temporarily locked for 10 minutes.",
        "booking_id": new_booking.booking_id,
        "show_id": new_booking.show_id,
        "booking_status": new_booking.booking_status,
        "total_amount": new_booking.total_amount,
        "lock_expires_at": lock_expiration_time,
        "items": [
            {"booking_item_id": item.booking_item_id, "show_seat_id": item.show_seat_id, "price": item.price} 
            for item in booking_items]
    }


# modify booking items
def delete_booking_item(booking_id: UUID, booking_item_id: UUID, current_user_id: UUID, db: Session):
    booking = db.query(SQbooking_section).filter(SQbooking_section.booking_id == booking_id,SQbooking_section.user_id == current_user_id).first()
    if not booking:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Booking section not found or unauthorized.")

    if booking.booking_status != "Pending":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Cannot modify items for a non-pending booking.")

    item = db.query(SQbooking_items).filter(SQbooking_items.booking_item_id == booking_item_id,SQbooking_items.booking_id == booking_id ).first()
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Booking item not found in this order.")

    show_seat = db.query(SQshow_seats).filter(SQshow_seats.show_seat_id == item.show_seat_id).first()
    if show_seat:
        show_seat.status = "available"
        show_seat.lock_expires_at = None

    item_price = item.price
    db.delete(item)
    db.flush()

    booking.total_amount -= item_price
    if booking.total_amount <= 0:
        booking.booking_status = "Cancelled"

    db.commit()

    return  {"message": "Booking item removed successfully. Seat lock released.","booking_id": booking.booking_id,"new_total_amount": booking.total_amount}


from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.show_seats import SQshow_seats
from app.schemas.show_seats import SeatBookingRequest

from app.models.seats import SQseats
from app.models.shows import SQshows

#--------------------------------------------------------show_seats----------------------------------------------------

# to genrate seats for show 
def generate_show_seats_for_show(show_id: int, screen_id: int, base_price: float, db: Session):
    physical_seats = db.query(SQseats).filter(SQseats.screen_id == screen_id).all()
    if not physical_seats:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Cannot schedule show: No physical seats found for this screen. Create screen seats first.")

    show_seats_list = [
        SQshow_seats(show_id=show_id,seat_id=seat.id,  price=base_price,status="available")
        for seat in physical_seats
    ]

    db.add_all(show_seats_list)
    db.commit()


# to view show seats 
def get_show_seats(show_id: int, db: Session):
    show = db.query(SQshows).filter(SQshows.show_id == show_id).first()
    if not show:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Show not found")
    
    now = datetime.now()

    expired_locks = db.query(SQshow_seats).filter(SQshow_seats.show_id == show_id,SQshow_seats.status == "locked",SQshow_seats.lock_expires_at < now).all()
    for seat in expired_locks: 
        seat.status = "available" 
        seat.lock_expires_at = None
    
    if expired_locks:

        db.commit()

    show_seats_data = db.query(SQshow_seats, SQseats).join( SQseats, SQshow_seats.seat_id == SQseats.id).filter(SQshow_seats.show_id == show_id).all()

    if not show_seats_data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No seats found for this show. Ensure physical seats exist for this screen before scheduling." )
    
    result = []

    for ss, seat in show_seats_data:
        if ss.status == "available":
            availability_text = "available to book"
        elif ss.status == "locked":
            availability_text = "currently locked (temporary hold)"
        else:
            availability_text = "already booked"

        result.append({
            "show_seat_id": ss.show_seat_id,
            "show_id": ss.show_id,
            "seat_id": ss.seat_id,
            "row_name": seat.seat_row,
            "seat_number": seat.seat_number, 
            "seat_type": seat.seat_type,    
            "price": ss.price,
            "status": ss.status,
            "description": f"Seat {seat.seat_row}{seat.seat_number} is {availability_text}"
        })

    return result


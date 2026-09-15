from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.seats import SQseats
from app.schemas.seats import SeatCreate
from uuid import UUID

from app.models.screens import SQscreens

#-------------------------------------------------------------seats-------------------------------------------------------------#

# to genrate seats for screen
def generate_seats_for_screen(hall: SeatCreate, db: Session):

    screen = db.query(SQscreens).filter(SQscreens.theater_id == hall.theater_id,SQscreens.screen_id == hall.screen_id).first()
    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found in theater")

    new_seats = []
    for row in hall.rows:
        for seat_num in range(1, hall.seats_per_row + 1):
            seat_number_str = f"{row}{seat_num}"

            seat = SQseats(
                theater_id=hall.theater_id,
                screen_id=screen.screen_id,      
                seat_row=row,
                seat_number=seat_number_str,     
                seat_type=hall.seat_type)
            
            new_seats.append(seat)        

    try:
        db.add_all(new_seats)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException( status.HTTP_500_INTERNAL_SERVER_ERROR,  detail=f"Failed to generate seats: {e}")

    return "Successfully generated local seats for screen"


# to update seats 
def update_seats_for_screen(theater_id: UUID, screen_id: UUID, new_seat_type: str, db: Session):

    screen = db.query(SQscreens).filter(SQscreens.theater_id == theater_id,SQscreens.screen_id == screen_id).first()
    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found in this theater")

    updated_count = db.query(SQseats).filter(SQseats.screen_id == screen.screen_id).update({SQseats.seat_type: new_seat_type},  synchronize_session=False )
    try:
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update screen seats: {e}" )

    return f"Successfully updated {updated_count} seats to '{new_seat_type}' for screen {screen_id}"


# to delete seats 
def delete_seats_for_screen(theater_id: UUID, screen_id: UUID, db: Session):
    
    screen = db.query(SQscreens).filter(SQscreens.theater_id == theater_id,  SQscreens.screen_id == screen_id).first()
    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found in this theater")

    deleted_count = db.query(SQseats).filter(SQseats.screen_id == screen.screen_id).delete()
    
    try:
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException( status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete seats for screen: {e}" )

    return f"Successfully deleted {deleted_count} seats for screen {screen_id}"

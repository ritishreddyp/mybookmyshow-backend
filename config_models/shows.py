from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Date,Time,Float
from datetime import datetime
from config import Base
from sqlalchemy.orm import relationship

class SQshows(Base):

    __tablename__ = "Shows"
    show_id = Column(Integer,primary_key=True,autoincrement=True)
    screen_id = Column(Integer,ForeignKey("Screens.screen_id"),nullable=False)
    movie_id = Column(Integer,ForeignKey("Movies.movie_id"),nullable=False)
    language_id = Column(Integer,ForeignKey("languages.language_id"),nullable=False)
    show_date = Column(Date, nullable=False)
    show_time = Column(Time, nullable=False)
    base_price = Column(Float, nullable=False)
    status = Column(String,default="Scheduled", nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    screen = relationship("SQscreens", back_populates="shows")
    movie = relationship("SQmovies", back_populates="shows")
    language = relationship("SQlanguages", back_populates="shows")

    show_seats = relationship("SQshow_seats", back_populates="show", cascade="all, delete-orphan")
    bookings = relationship("SQbooking_section", back_populates="show")
    tickets = relationship("SQtickets", back_populates="show")
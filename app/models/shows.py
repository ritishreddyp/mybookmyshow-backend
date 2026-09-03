from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Time, Float,Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base

class SQshows(Base):
    __tablename__ = "Shows"

    show_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("Movies.movie_id", ondelete="CASCADE"), nullable=False)
    screen_id = Column(Integer, ForeignKey("Screens.id", ondelete="CASCADE"), nullable=False)
    language_id = Column(Integer, ForeignKey("Languages.language_id", ondelete="CASCADE"), nullable=False)
    show_date = Column(Date, nullable=False)
    show_time = Column(Time, nullable=False)
    base_price = Column(Float, nullable=False)
    status = Column(String, default="active", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    screen = relationship("SQscreens", back_populates="shows")
    movie = relationship("SQmovies", back_populates="shows")
    language = relationship("SQlanguages", back_populates="shows")
    show_seats = relationship("SQshow_seats", back_populates="show", cascade="all, delete-orphan")
    bookings = relationship("SQbooking_section", back_populates="show")
    tickets = relationship("SQtickets", back_populates="show")


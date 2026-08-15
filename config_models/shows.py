from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Date,Time,Float
from datetime import datetime
from config import Base


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
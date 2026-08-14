from sqlalchemy import Column, Integer, String, Float
from config import Base

class cities(Base):

    __tablename__ = "Cities"
    cities_id = Column(Integer,primary_key =True, autoincrement=True)
    city_name = Column(String, nullable=False)
    state = Column(String, nullable=False)
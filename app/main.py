from fastapi import FastAPI
from app.api.main import api_router
from app.core.db import Base , engine

from app.models import SQUser,SQcity,SQmovies,SQlanguages,SQtheaters,SQscreens,SQseats,SQshows,SQshow_seats,SQbooking_section,SQbooking_items,SQpayments,SQtickets


Base.metadata.create_all(bind=engine)


app = FastAPI(title="My BookMyShow API")

app.include_router(api_router)


from fastapi import FastAPI
from app.api.main import api_router
from app.core.db import Base , engine

from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.models import SQUser,SQcity,SQmovies,SQlanguages,SQtheaters,SQscreens,SQseats,SQshows,SQshow_seats,SQbooking_section,SQbooking_items,SQpayments,SQtickets


Base.metadata.create_all(bind=engine)

app = FastAPI(title="My BookMyShow API")

IMAGE_DIR = Path(r"C:\Users\HP\OneDrive\Documents\movie_images")
app.mount("/images", StaticFiles(directory=str(IMAGE_DIR)), name="images")

app.include_router(api_router)



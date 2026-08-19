from fastapi import APIRouter
from app.api.routes import auth, bookings, cities, movies, shows, users


api_router = APIRouter()

api_router.include_router( auth.router, prefix="/auth", tags=["Authentication"] )
api_router.include_router( users.router, prefix="/users", tags=["Users"] )
api_router.include_router( cities.router, prefix="/cities", tags=["Cities"] )
api_router.include_router( movies.router, prefix="/movies", tags=["Movies"] )
api_router.include_router( shows.router, prefix="/shows", tags=["Shows & Seat Matrix"] )
api_router.include_router( bookings.router, prefix="/bookings", tags=["Bookings & Payments"] )
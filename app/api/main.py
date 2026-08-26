from fastapi import APIRouter
from app.api.routers import auth, users,cities,movies,languages,theaters,seats,shows,show_seats,bookings,payments,tickets

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"]) 
api_router.include_router(cities.router, prefix="/city" , tags=["City"])
api_router.include_router( movies.router, prefix="/movies", tags=["Movies"] )
api_router.include_router(languages.router, prefix="/languages", tags=["Languages"])
api_router.include_router(theaters.router, prefix="/theaters", tags=["theaters"])
api_router.include_router(seats.router, prefix="/seats", tags=["seats"])
api_router.include_router(shows.router, prefix="/shows", tags=["shows"])
api_router.include_router(show_seats.router, prefix="/show_seats", tags=["show_seats"])
api_router.include_router(bookings.router,prefix="/bookings", tags=["Bookings & Cart"])
api_router.include_router(payments.router,prefix="/payments", tags=["payments"])
api_router.include_router(tickets.router,prefix="/tickets", tags=["tickets"])
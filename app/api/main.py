from fastapi import APIRouter
from app.api.routers import auth, users,cities,movies,languages

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"]) 
api_router.include_router(cities.router, prefix="/city" , tags=["City"])
api_router.include_router( movies.router, prefix="/movies", tags=["Movies"] )
api_router.include_router(languages.router, prefix="/languages", tags=["Languages"])
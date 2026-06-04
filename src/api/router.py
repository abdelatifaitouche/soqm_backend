from fastapi import APIRouter
from src.features.auth.routes.auth_routes import router as auth_router

router = APIRouter(prefix="/api/v1")


router.include_router(auth_router)

from fastapi import APIRouter
from src import admin, lockers

router = APIRouter()
router.include_router(admin.router)
router.include_router(lockers.router)
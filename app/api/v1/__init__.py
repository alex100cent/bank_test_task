from fastapi import APIRouter

from . import demo, monitoring, wallet

router = APIRouter()
router.include_router(monitoring.router, tags=["monitoring"])
router.include_router(demo.router, tags=["demo"])
router.include_router(wallet.router, tags=["wallet"])

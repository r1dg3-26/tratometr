from aiogram import Router
from . import start, decrease

router = Router()
router.include_router(start.router)
router.include_router(decrease.router)
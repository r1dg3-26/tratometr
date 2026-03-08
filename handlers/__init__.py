from aiogram import Router
from . import operations, register

router = Router()
router.include_router(register.router)
router.include_router(operations.router)
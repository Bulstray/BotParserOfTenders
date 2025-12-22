from aiogram import Bot, Dispatcher
from core.config import settings
from routers import router

bot: Bot = Bot(token=settings.token)
dp: Dispatcher = Dispatcher()

dp.include_router(
    router,
)

from aiogram import Bot, Dispatcher

from core.config import settings

bot_settings = Bot(token=settings.bot_settings.token)
dp = Dispatcher()

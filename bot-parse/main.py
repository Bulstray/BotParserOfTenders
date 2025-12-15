import asyncio

from bot import bot_settings, dp


async def main() -> None:
    await bot_settings.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot_settings)


if __name__ == "__main__":
    asyncio.run(main())

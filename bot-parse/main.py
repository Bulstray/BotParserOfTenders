import asyncio

from bot import bot_settings, dp
from aiogram.enums import ParseMode

from parsers.check_new_post import checks_in_database
from core.config import settings


async def main() -> None:
    await bot_settings.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(hour_parce())
    await dp.start_polling(bot_settings)


async def hour_parce():
    while True:
        await asyncio.sleep(settings.time_pause.parsing_frequency)
        new_posts = checks_in_database()
        if new_posts:

            for post in new_posts:

                text = "📌 Новый Тендер\n────────────────────\n\n"

                for k, v in post.items():
                    text = f"{text}<b>{k.capitalize()}</b>: {v}\n"

                text = f"{text.rstrip()}\n\n────────────────────"

                # await bot_settings.send_message(
                #     chat_id=1023172486,
                #     text=text,
                #     parse_mode=ParseMode.HTML,
                # )

                await asyncio.sleep(0.05)


if __name__ == "__main__":
    asyncio.run(main())

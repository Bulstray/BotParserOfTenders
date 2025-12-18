from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

import asyncio

from parsers.lukhoil import parce_lukhoil

from parsers.check_new_post import checks_in_database

router: Router = Router()

WELCOME_MESSAGE = """
<b>🔍 Парсер бот</b>

<code>━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>Мониторинг сайтов</b>
по вашим ключевым словам

"""


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        text=WELCOME_MESSAGE,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


# @router.message(F.text)
# async def parse_for_keyword(message: Message) -> None:
#     etp_gpb = EtpGpb(message.text)
#     # for text in etp_gpb.parse_etp_gpb():
#     #
#     #     if text:
#     #         await asyncio.sleep(0.05)
#     #         await message.answer(
#     #             text=text.lstrip(),
#     #             parse_mode=ParseMode.HTML,
#     #         )
#
#     for text in parce_lukhoil(message.text):
#         await asyncio.sleep(0.05)
#         await message.answer(
#             text=text.lstrip(),
#             parse_mode=ParseMode.HTML,
#         )

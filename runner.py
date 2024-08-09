import logging
import asyncio
from aiogram import Dispatcher, Bot
from config import BOT_TOKEN
from handlers import command_router
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
async def main():
    dp = Dispatcher()
    dp.include_router(command_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')
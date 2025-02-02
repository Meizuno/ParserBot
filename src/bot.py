from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import TOKEN, CHAT_IDS
from src.logger import logger


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def bot_message(message: str) -> None:
    """Send message to all users"""

    for chat_id in CHAT_IDS:
        await bot.send_message(chat_id, message)
        logger.info("Message '%s' sent to '%s'", message, chat_id)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command"""

    await message.answer(f"Your chat id: {html.bold(message.chat.id)}")

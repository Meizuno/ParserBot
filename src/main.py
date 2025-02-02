import asyncio

from src.bot import dp, bot
from src.logger import logger
from src.parser import create_db, parse_anime


async def periodic_task(func: callable, interval: int):
    """Periodic task"""

    logger.info("Scheduled '%s' ...", func.__name__)
    while True:
        await func()
        await asyncio.sleep(interval)


async def main() -> None:
    """Start the bot"""

    asyncio.create_task(periodic_task(parse_anime, 3600))

    logger.info("Bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    create_db()
    asyncio.run(main())

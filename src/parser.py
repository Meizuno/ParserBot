import aiohttp
import requests
from bs4 import BeautifulSoup
from sqlmodel import SQLModel
from src.models import ParsedURL, ParsedItem, engine
from src.bot import bot_message


def create_db() -> None:
    """Create database"""

    SQLModel.metadata.create_all(engine)


async def parse_anime() -> str:
    """Parse anime url"""

    base_url = "https://jut.su"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    for parsed_url in ParsedURL.all():
        response = requests.get(parsed_url.url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")
        result = soup.find_all("i", string=parsed_url.key)
        items = [item.parent for item in result]

        for item in items:
            is_exists = ParsedItem.exists(base_url + item["href"], item.text)
            if not is_exists:
                parsed_item = ParsedItem.create(base_url + item["href"], item.text)
                async with aiohttp.ClientSession(headers=headers) as _:
                    await bot_message(parsed_item.url)

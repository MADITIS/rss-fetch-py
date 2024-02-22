from dotenv import dotenv_values
from pydantic import ValidationError
from src.models import Config
from pyrogram.client import Client


config_dict = dotenv_values()
try:
    config = Config(**config_dict)  # type: ignore
except ValidationError as e:
    print(f"One or more env vars are missing {e!s}")

app = Client(
    name="rss",
    api_id=config.api_id,
    api_hash=config.api_hash,
    bot_token=config.bot_token,
)

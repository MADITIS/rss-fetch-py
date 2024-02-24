from dotenv import dotenv_values
from pydantic import ValidationError
from src.models import Config
from pyrogram.client import Client
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
config_dict = dotenv_values()
try:
    config = Config(**config_dict)  # type: ignore
    logger.info("Parsed Config!")
except ValidationError as e:
    logger.exception(f"One or more env vars are missing {e!s}")

app = Client(
    name="rss",
    api_id=config.api_id,
    api_hash=config.api_hash,
    bot_token=config.bot_token,
)

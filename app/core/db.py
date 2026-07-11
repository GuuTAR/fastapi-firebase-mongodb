from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.core.config import get_settings
from app.models.user import User

_client: AsyncMongoClient | None = None


async def init_db() -> None:
    global _client
    settings = get_settings()
    _client = AsyncMongoClient(settings.mongodb_uri)
    await init_beanie(
        database=_client[settings.mongodb_db],
        document_models=[User],
    )


async def close_db() -> None:
    if _client is not None:
        await _client.close()

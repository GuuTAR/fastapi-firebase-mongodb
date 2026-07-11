import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api.router import api_router
from app.api.routes import system
from app.core.config import get_settings
from app.core.db import close_db, init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    app.state.http_client = httpx.AsyncClient(timeout=10.0)
    try:
        # Pay the DNS/TLS handshake cost at startup instead of on the first
        # request to Firebase's Identity Toolkit REST API.
        await app.state.http_client.get("https://identitytoolkit.googleapis.com/")
    except httpx.HTTPError as exc:
        logger.warning("Failed to warm up Identity Toolkit connection: %s", exc)

    yield

    await app.state.http_client.aclose()
    await close_db()


settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
app.include_router(system.router)
app.include_router(api_router)

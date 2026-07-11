from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "fastapi-firebase-mongodb"
    debug: bool = False

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "fastapi_firebase_mongodb"

    # Firebase service account fields. Leave unset to fall back to
    # Application Default Credentials (e.g. GOOGLE_APPLICATION_CREDENTIALS).
    firebase_project_id: str | None = None
    firebase_private_key_id: str | None = None
    firebase_private_key: str | None = None
    firebase_client_email: str | None = None

    # Web API key from the Firebase project settings. Required for the
    # email/password sign-in REST call (the Admin SDK cannot do this).
    firebase_web_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()

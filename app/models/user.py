from beanie import Document
from pydantic import Field


class User(Document):
    # Must match the "uid" claim from the verified Firebase ID token.
    firebase_uid: str = Field(..., description="Firebase Auth UID, unique per user")
    email: str | None = None
    display_name: str | None = None

    class Settings:
        name = "users"
        indexes = ["firebase_uid"]

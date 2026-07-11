from pydantic import BaseModel, EmailStr, Field


class GetFirebaseTokenRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class GetFirebaseTokenResponse(BaseModel):
    token: str
    expires_in: int


class GetFirebaseUserResponse(BaseModel):
    uid: str
    email: str | None = None
    display_name: str | None = None
    photo_url: str | None = None

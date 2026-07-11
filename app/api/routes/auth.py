import httpx
from fastapi import APIRouter, HTTPException, Request, status
from firebase_admin import auth

from app.core.config import get_settings
from app.core.security import CurrentUser, get_firebase_app
from app.schemas.auth import (
    GetFirebaseTokenRequest,
    GetFirebaseTokenResponse,
    GetFirebaseUserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])

_SIGN_IN_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


@router.get("/me", response_model=GetFirebaseUserResponse)
async def get_firebase_user(current_user: CurrentUser) -> GetFirebaseUserResponse:
    get_firebase_app()
    user_record = auth.get_user(current_user["uid"])
    return GetFirebaseUserResponse(
        uid=user_record.uid,
        email=user_record.email,
        email_verified=user_record.email_verified,
        display_name=user_record.display_name,
        phone_number=user_record.phone_number,
        photo_url=user_record.photo_url,
        disabled=user_record.disabled,
    )


@router.post("/token", response_model=GetFirebaseTokenResponse)
async def get_firebase_token(
    payload: GetFirebaseTokenRequest, request: Request
) -> GetFirebaseTokenResponse:
    settings = get_settings()
    if not settings.firebase_web_api_key:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="FIREBASE_WEB_API_KEY is not configured",
        )

    client: httpx.AsyncClient = request.app.state.http_client
    try:
        response = await client.post(
            _SIGN_IN_URL,
            params={"key": settings.firebase_web_api_key},
            json={
                "email": payload.email,
                "password": payload.password,
                "returnSecureToken": True,
            },
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to reach Firebase authentication service",
        ) from exc

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    data = response.json()

    return GetFirebaseTokenResponse(
        token=data["idToken"],
        expires_in=data["expiresIn"],
    )

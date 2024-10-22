from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
import os
from services.users import create_user, get_user_by_email 
from database import get_async_session  


load_dotenv()

router = APIRouter(prefix="/auth")


CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/callback"

@router.get("/login")
async def login():
    authorization_url = (
        "https://accounts.google.com/o/oauth2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        "response_type=code&"
        "scope=openid profile email"
    )
    return RedirectResponse(url=authorization_url)

@router.get("/callback")
async def callback(code: str, session: AsyncSession = Depends(get_async_session)):
    async with AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=token_response.status_code, detail=token_response.text)

        token_data = token_response.json()

        if "error" in token_data:
            raise HTTPException(status_code=400, detail=token_data["error"])

        try:
            id_info = id_token.verify_oauth2_token(token_data['id_token'], requests.Request(), CLIENT_ID)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        user_email = id_info.get('email').lower()
        user_name = id_info.get('name')

        existing_user = await get_user_by_email(session, user_email)

        if not existing_user:
            await create_user(session, user_email, user_name, "")

        return {
            "access_token": token_data["access_token"],
            "expires_in": token_data["expires_in"],
            "user_email": user_email,
            "user_name": user_name
        }

@router.get("/userinfo")
async def get_user_info(token: str):
    async with AsyncClient() as client:
        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token}"}
        )
        if user_info_response.status_code != 200:
            raise HTTPException(status_code=user_info_response.status_code, detail=user_info_response.text)

        return user_info_response.json()

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
import requests
from config import settings
import json

app = FastAPI()

# Stepik OAuth2 данные
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
REDIRECT_URI = "http://localhost:8000/auth/stepik/callback"

# OAuth2 конфигурация для Stepik
AUTHORIZATION_URL = "https://stepik.org/oauth2/authorize/"
TOKEN_URL = "https://stepik.org/oauth2/token/"
USER_INFO_URL = "https://stepik.org/api/users/me"

# Хранилище токенов и сессий
user_sessions = {}

# OAuth2 схема (опционально)
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_URL,
    tokenUrl=TOKEN_URL,
)


def get_token():
    auth = requests.auth.HTTPBasicAuth(settings.CLIENT_ID, settings.CLIENT_SECRET)
    resp = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
    token = json.loads(resp.text)['access_token']
    return token


token = get_token()


@app.get("/login/stepik")
async def login_stepik():
    """
    Направляет пользователя на страницу авторизации Stepik.
    """
    auth_url = (
        f"{AUTHORIZATION_URL}?response_type=code&client_id={CLIENT_ID}"
    )
    return RedirectResponse(auth_url)


@app.get("/auth/stepik/callback")
async def stepik_callback(code: str):
    """
    Обрабатывает колбэк после авторизации Stepik и получает токен.
    """
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    # Обменять код на токен
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    token_resp = requests.post(TOKEN_URL, data=data).json()

    access_token = token_resp.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=400, detail="Failed to retrieve access token"
        )

    # Получить данные о пользователе
    user_resp = requests.get(
        USER_INFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    user = user_resp.get("users", [None])[0]
    if not user:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")

    # Сохранить токен и данные о пользователе (в данном случае в памяти)
    user_sessions[user["id"]] = {
        "access_token": access_token,
        "refresh_token": token_resp.get("refresh_token"),
        "user_info": user,
    }

    return JSONResponse(
        content={
            "message": f"Welcome, {user['profile']['first_name']} {user['profile']['last_name']}!",
            "user_id": user["id"],
        }
    )


@app.get("/me")
async def get_current_user(user_id: int):
    """
    Возвращает информацию о текущем авторизованном пользователе.
    """
    user_session = user_sessions.get(user_id)
    if not user_session:
        raise HTTPException(status_code=404, detail="User not found or not logged in")

    return {
        "user_info": user_session["user_info"],
        "access_token": user_session["access_token"],
    }

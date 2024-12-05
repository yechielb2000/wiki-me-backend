from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyCookie
from fastapi_csrf_protect import CsrfProtect
from loguru import logger
from pydantic_settings import BaseSettings

from app.models.player import Player
from app.services.env_vars import CSRF_SECRET_KEY

csrf_header = APIKeyCookie(name="fastapi-csrf-token")


class CsrfSettings(BaseSettings):
    secret_key: str = CSRF_SECRET_KEY


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=Player, tags=["auth"])
async def login(request: Request, name: str):
    """
    Creating player.
    Player is the entity for the user, we use the player id to validate its sessions.
    """
    # TODO: if already logged in you should not let him login again
    player = Player(id=await Player.generate_id(), name=name)
    await player.create()
    return player


@auth_router.get("/csrf-token", tags=["csrf"])
async def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    token, signed = csrf_protect.generate_csrf_tokens()
    response = JSONResponse(status_code=200, content={'csrf_token': signed})
    csrf_protect.set_csrf_cookie(signed, response)
    return response


async def validate_csrf(request: Request, csrf_protect: CsrfProtect = Depends()):
    try:
        print(request.cookies)
        await csrf_protect.validate_csrf(request, secret_key=CSRF_SECRET_KEY)
    except Exception as e:
        logger.warning(f'User CSRF token validation failed', request=request, csrf_protect=csrf_protect)
        raise HTTPException(status_code=403, detail="CSRF validation failed")



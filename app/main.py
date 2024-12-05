from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError

from app.logger_setup import setup_logger
from app.routers import games_router, auth_router
from app.routers.auth import validate_csrf, csrf_header

app = FastAPI(title='Wiki Me API', on_startup=[setup_logger])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change on production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware('http')
# async def player_session(request: Request, call_next):
#     player_id = request.headers.get('Player-ID')  # TODO should I use my own header or cookies?
#
#     if not player_id:
#         return RedirectResponse('/auth/login', status_code=status.HTTP_401_UNAUTHORIZED)
#
#     if not Player.exists(player_id):
#         logger.warning(f'Player {player_id} does not exist', request=request)
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or does not exist")
#
#     response = await call_next(request)
#     response.headers['Player-ID'] = player_id
#     return response


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.message})


app.include_router(auth_router)
app.include_router(games_router, dependencies=[Depends(validate_csrf), Depends(csrf_header)])


@app.get('/')
def main(request: Request):
    return {'hello world'}

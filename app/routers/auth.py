from fastapi import APIRouter

LIFETIME_SECONDS = 3600

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# cookie_secure = True for SSL | cookie_samesite to avoid csrf

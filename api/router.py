from fastapi import APIRouter

from api.routes import auth, chat, health, providers

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(providers.router, prefix="/providers", tags=["providers"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

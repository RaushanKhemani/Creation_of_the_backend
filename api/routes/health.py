from datetime import datetime, timezone

from fastapi import APIRouter
from sqlalchemy import text

from config import get_settings
from db.session import SessionLocal

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    settings = get_settings()
    return {
        "success": True,
        "data": {
            "status": "ok",
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


@router.get("/health/ready")
def readiness_check() -> dict:
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
    return {"success": True, "data": {"status": "ready"}}

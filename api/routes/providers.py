from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_db, require_roles
from db.models.user import User
from schemas.provider import ProviderCreate, ProviderRead
from services.provider_service import create_provider, get_provider_by_key, list_providers

router = APIRouter()


@router.get("")
def get_providers(db: Session = Depends(get_db), _: User = Depends(require_roles("user", "admin"))) -> dict:
    providers = list_providers(db)
    return {"success": True, "data": [ProviderRead.model_validate(item).model_dump() for item in providers]}


@router.get("/{provider_key}")
def get_provider(
    provider_key: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("user", "admin")),
) -> dict:
    provider = get_provider_by_key(db, provider_key)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return {"success": True, "data": ProviderRead.model_validate(provider).model_dump()}


@router.post("", status_code=status.HTTP_201_CREATED)
def add_provider(
    payload: ProviderCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
) -> dict:
    created = create_provider(db, payload)
    if not created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Provider key already exists")
    return {"success": True, "data": ProviderRead.model_validate(created).model_dump()}

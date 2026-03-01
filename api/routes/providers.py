from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from db.models.user import User
from schemas.provider import ProviderCreate, ProviderRead
from services.provider_service import create_provider, get_provider_by_key, list_providers

router = APIRouter()


@router.get("", response_model=list[ProviderRead])
def get_providers(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[ProviderRead]:
    providers = list_providers(db)
    return [ProviderRead.model_validate(item) for item in providers]


@router.get("/{provider_key}", response_model=ProviderRead)
def get_provider(provider_key: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> ProviderRead:
    provider = get_provider_by_key(db, provider_key)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return ProviderRead.model_validate(provider)


@router.post("", response_model=ProviderRead, status_code=status.HTTP_201_CREATED)
def add_provider(
    payload: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProviderRead:
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Superuser required")

    created = create_provider(db, payload)
    if not created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Provider key already exists")
    return ProviderRead.model_validate(created)

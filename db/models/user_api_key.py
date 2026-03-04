from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class UserAPIKey(Base):
    __tablename__ = "user_api_keys"
    __table_args__ = (
        UniqueConstraint("user_id", "api_key_hash", name="uq_user_api_key_hash"),
        Index("ix_user_api_keys_user_id_updated_at", "user_id", "updated_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    provider_name: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_key: Mapped[str] = mapped_column(String(64), nullable=False)
    api_key_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    api_key_masked: Mapped[str] = mapped_column(String(64), nullable=False)
    encrypted_api_key: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), index=True
    )

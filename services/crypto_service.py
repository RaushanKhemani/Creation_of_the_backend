from cryptography.fernet import Fernet

from config import get_settings


def _get_fernet() -> Fernet:
    settings = get_settings()
    return Fernet(settings.api_key_encryption_key)


def encrypt_text(plain_text: str) -> str:
    return _get_fernet().encrypt(plain_text.encode("utf-8")).decode("utf-8")


def decrypt_text(cipher_text: str) -> str:
    return _get_fernet().decrypt(cipher_text.encode("utf-8")).decode("utf-8")

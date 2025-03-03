import hashlib


def encrypt_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

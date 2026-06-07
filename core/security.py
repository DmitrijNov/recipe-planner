from pwdlib import PasswordHash

# Argon2-backed hasher (pwdlib's recommended default).
_password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a password using Argon2."""
    return _password_hash.hash(password)


def verify_password(password: str, stored: str) -> bool:
    """Check ``password`` against a hash produced by :func:`hash_password`."""
    return _password_hash.verify(password, stored)

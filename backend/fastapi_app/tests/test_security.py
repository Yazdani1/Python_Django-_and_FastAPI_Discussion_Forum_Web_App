import pytest
from fastapi_app.core.security import JWTHandler, PasswordHandler


def test_password_hash_is_not_plain() -> None:
    hashed = PasswordHandler.hash("secret123")
    assert hashed != "secret123"


def test_password_verify_correct() -> None:
    plain = "mypassword"
    hashed = PasswordHandler.hash(plain)
    assert PasswordHandler.verify(plain, hashed) is True


def test_password_verify_wrong() -> None:
    hashed = PasswordHandler.hash("correct")
    assert PasswordHandler.verify("wrong", hashed) is False


def test_create_and_decode_access_token() -> None:
    token = JWTHandler.create_access_token(subject="user-42")
    payload = JWTHandler.decode_token(token)
    assert payload["sub"] == "user-42"
    assert payload["type"] == "access"


def test_create_and_decode_refresh_token() -> None:
    token = JWTHandler.create_refresh_token(subject="user-42")
    payload = JWTHandler.decode_token(token)
    assert payload["sub"] == "user-42"
    assert payload["type"] == "refresh"


def test_get_subject_from_token() -> None:
    token = JWTHandler.create_access_token(subject="user-99")
    subject = JWTHandler.get_subject(token)
    assert subject == "user-99"


def test_decode_invalid_token_raises() -> None:
    with pytest.raises(ValueError, match="Invalid or expired token"):
        JWTHandler.decode_token("not.a.real.token")


def test_access_token_extra_claims() -> None:
    token = JWTHandler.create_access_token(subject="1", extra_claims={"role": "admin"})
    payload = JWTHandler.decode_token(token)
    assert payload["role"] == "admin"

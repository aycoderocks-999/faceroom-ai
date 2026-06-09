from app.core.security import create_access_token, decode_token, hash_password, verify_password


def test_password_hashing():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_tokens():
    token = create_access_token("42")
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "42"
    assert payload["type"] == "access"


def test_register_and_login(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"email": "user@test.com", "username": "user1", "password": "securepass1"},
    )
    assert res.status_code == 201
    assert res.json()["email"] == "user@test.com"

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "user@test.com", "password": "securepass1"},
    )
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_protected_route_requires_auth(client):
    res = client.get("/api/v1/rooms")
    assert res.status_code == 403

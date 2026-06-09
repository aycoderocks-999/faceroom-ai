def test_create_and_join_room(client, auth_headers):
    create = client.post(
        "/api/v1/rooms/create",
        json={"room_name": "Test Event"},
        headers=auth_headers,
    )
    assert create.status_code == 201
    data = create.json()
    assert data["room_name"] == "Test Event"
    assert data["room_code"].startswith("ROOM-")

    client.post(
        "/api/v1/auth/register",
        json={"email": "joiner@test.com", "username": "joiner", "password": "password123"},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "joiner@test.com", "password": "password123"},
    )
    joiner_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    join = client.post(
        "/api/v1/rooms/join",
        json={"room_code": data["room_code"]},
        headers=joiner_headers,
    )
    assert join.status_code == 200
    assert join.json()["id"] == data["id"]


def test_list_rooms(client, auth_headers):
    client.post("/api/v1/rooms/create", json={"room_name": "Room A"}, headers=auth_headers)
    res = client.get("/api/v1/rooms", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1

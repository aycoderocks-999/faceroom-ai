def test_health_endpoint(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

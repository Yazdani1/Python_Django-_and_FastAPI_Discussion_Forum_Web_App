import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_returns_200(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_check_response_shape(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    body = response.json()
    assert body["success"] is True
    assert "message" in body
    assert body["data"]["status"] == "ok"


@pytest.mark.asyncio
async def test_health_check_message(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    body = response.json()
    assert isinstance(body["message"], str)
    assert len(body["message"]) > 0

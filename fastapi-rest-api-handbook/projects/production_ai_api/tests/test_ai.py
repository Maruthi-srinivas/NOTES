import os

import pytest
from httpx import ASGITransport, AsyncClient

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://app:change-me@localhost:5432/ai_test",
)
os.environ.setdefault("JWT_SECRET", "test-only-secret")
os.environ.setdefault("DEMO_PASSWORD", "change-me")
os.environ["QUOTA_LIMIT"] = "50"

from app.db import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture
async def client():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http:
        yield http


async def bearer(client: AsyncClient, tenant: str) -> dict[str, str]:
    response = await client.post("/auth/token", json={"tenant": tenant, "password": "change-me"})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.mark.asyncio
async def test_rag_is_tenant_isolated(client: AsyncClient) -> None:
    alpha = await bearer(client, "alpha")
    beta = await bearer(client, "beta")
    created = await client.post(
        "/v1/documents",
        json={"title": "Note", "body": "alpha-secret lives in this passage"},
        headers=alpha,
    )
    assert created.status_code == 201
    leaked = await client.post("/v1/query", json={"message": "where is the secret"}, headers=beta)
    assert leaked.status_code == 200
    assert "alpha-secret" not in leaked.json()["answer"]
    found = await client.post("/v1/query", json={"message": "where is the secret"}, headers=alpha)
    assert "alpha-secret" in found.json()["answer"]


@pytest.mark.asyncio
async def test_tool_allow_list(client: AsyncClient) -> None:
    headers = await bearer(client, "alpha")
    denied = await client.post("/mcp/tools/call", json={"name": "shell", "text": "ls"}, headers=headers)
    assert denied.status_code == 403
    allowed = await client.post("/v1/agent", json={"name": "word_count", "text": "one two"}, headers=headers)
    assert allowed.status_code == 200
    assert allowed.json()["output"] == "2"


@pytest.mark.asyncio
async def test_stream_is_sse(client: AsyncClient) -> None:
    headers = await bearer(client, "alpha")
    response = await client.post("/v1/chat/stream", json={"message": "hello"}, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert "data:" in response.text

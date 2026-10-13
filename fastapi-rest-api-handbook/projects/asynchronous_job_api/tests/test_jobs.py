import os

import pytest
from httpx import ASGITransport, AsyncClient

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://app:change-me@localhost:5432/jobs_test",
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/1")

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


@pytest.mark.asyncio
async def test_duplicate_idempotency_key_returns_same_job(client: AsyncClient, monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeRedis:
        async def lpush(self, key: str, value: str) -> None:
            return None

    monkeypatch.setattr("app.main.redis_client", FakeRedis())
    body = {"task": "double", "value": 4, "idempotency_key": "same"}
    first = await client.post("/jobs", json=body)
    second = await client.post("/jobs", json=body)
    assert first.status_code == 202, first.text
    assert second.status_code == 202
    assert first.json()["id"] == second.json()["id"]
    assert first.json()["status"] == "QUEUED"


@pytest.mark.asyncio
async def test_cancel_queued_job(client: AsyncClient, monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeRedis:
        async def lpush(self, key: str, value: str) -> None:
            return None

    monkeypatch.setattr("app.main.redis_client", FakeRedis())
    created = await client.post("/jobs", json={"task": "double", "value": 1})
    job_id = created.json()["id"]
    cancelled = await client.post(f"/jobs/{job_id}/cancel")
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "CANCELLED"

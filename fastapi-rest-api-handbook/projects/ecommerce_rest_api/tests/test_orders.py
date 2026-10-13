import os

import pytest
from httpx import ASGITransport, AsyncClient

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://app:change-me@localhost:54329/ecommerce_test",
)
os.environ.setdefault("JWT_SECRET", "test-only-secret")
os.environ.setdefault("ADMIN_EMAILS", "admin@example.com")

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


async def register(client: AsyncClient, email: str, password: str = "password123") -> str:
    response = await client.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code == 201, response.text
    return response.json()["access_token"]


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_shopper_cannot_create_category(client: AsyncClient) -> None:
    token = await register(client, "shopper@example.com")
    response = await client.post("/categories", json={"name": "Pens"}, headers=auth(token))
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_order_is_idempotent_and_isolated(client: AsyncClient) -> None:
    admin = await register(client, "admin@example.com")
    category = await client.post("/categories", json={"name": "Pens"}, headers=auth(admin))
    assert category.status_code == 201
    product = await client.post(
        "/products",
        json={"name": "Blue pen", "price": "2.50", "stock": 5, "category_id": category.json()["id"]},
        headers=auth(admin),
    )
    assert product.status_code == 201, product.text
    product_id = product.json()["id"]

    shopper = await register(client, "buyer@example.com")
    other = await register(client, "other@example.com")
    payload = {"items": [{"product_id": product_id, "quantity": 2}]}
    headers = auth(shopper) | {"Idempotency-Key": "order-1"}
    first = await client.post("/orders", json=payload, headers=headers)
    second = await client.post("/orders", json=payload, headers=headers)
    assert first.status_code == 201, first.text
    assert second.status_code == 201
    assert first.json()["id"] == second.json()["id"]
    assert first.json()["total"] in {"5.00", "5.0"}

    listing = await client.get("/products")
    assert listing.status_code == 200
    assert listing.json()["items"][0]["stock"] == 3

    hidden = await client.get(f"/orders/{first.json()['id']}", headers=auth(other))
    assert hidden.status_code == 404


@pytest.mark.asyncio
async def test_missing_idempotency_key_is_rejected(client: AsyncClient) -> None:
    admin = await register(client, "admin@example.com")
    category = await client.post("/categories", json={"name": "Paper"}, headers=auth(admin))
    product = await client.post(
        "/products",
        json={"name": "Pad", "price": "1.00", "stock": 1, "category_id": category.json()["id"]},
        headers=auth(admin),
    )
    shopper = await register(client, "buyer@example.com")
    response = await client.post(
        "/orders",
        json={"items": [{"product_id": product.json()["id"], "quantity": 1}]},
        headers=auth(shopper),
    )
    assert response.status_code == 400

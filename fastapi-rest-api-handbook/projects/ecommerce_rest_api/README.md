# Project A: E-commerce REST API

Educational production-shaped API. Code in this project is meant to be executed with Docker Compose. Do not install the Python packages on the host.

## PRD

Shoppers register, browse products, and submit orders. Admins create categories and products. An order must not double-charge when the client retries. A shopper must not read another shopper's order.

## Requirements

Functional:

- Register and login with a bearer token.
- Admin-only category and product creation.
- Public product list with `limit`, `offset`, `category_id`, and `q`.
- Order creation that decrements stock in one transaction.
- `Idempotency-Key` required on order creation.
- Object-level order reads.

Nonfunctional:

- PostgreSQL is the system of record.
- Secrets come from the environment. `.env.example` holds placeholders only.
- Tests use `ecommerce_test`, never the app database, and drop tables only in that test database.

## Design

```mermaid
flowchart LR
  client[Client] --> api[FastAPI]
  api --> db[PostgreSQL]
```

`OAuth2PasswordBearer` only reads the bearer token. Login issues a signed JWT. Admin rights come from `ADMIN_EMAILS`, not from a client-supplied role field.

Order creation locks product rows with `SELECT ... FOR UPDATE`, checks stock, writes the order and an idempotency row, then commits. A repeated key returns the stored order and does not decrement stock again. Unknown orders and someone else's orders both return `404`.

## API

| Method | Path | Auth | Success |
| --- | --- | --- | --- |
| POST | `/auth/register` | no | 201 token |
| POST | `/auth/login` | no | 200 token |
| POST | `/categories` | admin | 201 |
| GET | `/categories` | no | 200 |
| POST | `/products` | admin | 201 |
| GET | `/products` | no | 200 page |
| POST | `/orders` | user + Idempotency-Key | 201 |
| GET | `/orders` | user | 200 own orders |
| GET | `/orders/{id}` | owner | 200 or 404 |
| GET | `/health` | no | 200 |

## Run

From this directory, with Docker running:

```bash
docker compose up --build
```

The API listens on `http://localhost:8000`. Interactive docs are at `/docs`.

Tests:

```bash
docker compose run --rm api pytest
```

Logs:

```bash
docker compose logs api
docker compose ps
```

Cleanup:

```bash
docker compose down -v
```

## Schema

Tables: `users`, `categories`, `products`, `orders`, `order_items`, `idempotency_records`. Uniqueness: email, category name, `(user_id, idempotency key)`.

This milestone creates tables at startup with `create_all`. A production deploy should replace that with Alembic and a migration step. That gap is intentional in this first milestone and is called out so it is not mistaken for a finished migration pipeline.

## Security notes

- Shoppers receive `403` for catalog writes.
- Order reads compare `user_id` on the server.
- Passwords are hashed with `pwdlib` recommended hash (Argon2 when the extra is installed).
- JWT secret is an environment variable. The compose file uses the example placeholder. Replace it before any shared deployment.
- Product search escapes `%` and `_`.

## Reliability notes

- Stock update and order insert share one transaction.
- Idempotency is stored in the database, so another API process can see it.
- This service does not retry payment captures. There is no payment provider.

## Troubleshooting

- `ecommerce_test` missing: the Postgres volume was created before `docker/init-test-db.sql` existed. Run `docker compose down -v` and start again.
- `401` on `/docs` authorize: the token URL is `/auth/login`, and the body is JSON, not the OAuth form. Use `/auth/register` or send the JSON login from curl.
- Healthcheck fails while Postgres is starting: wait for `pg_isready`.

## Interview prompts

1. Why is the idempotency record in the same transaction as the order?
2. Why does a foreign order return 404 instead of 403?
3. What breaks if stock is checked without a row lock?

Answers: (1) otherwise a crash can leave an order without a key or a key without an order. (2) 403 confirms the id exists. (3) two requests can both pass the stock check and oversell.

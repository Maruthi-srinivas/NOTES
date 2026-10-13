import json
from decimal import Decimal

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_session
from app.deps import current_user
from app.models import IdempotencyRecord, Order, OrderItem, Product, User
from app.schemas import OrderIn, OrderItemOut, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


def _to_out(order: Order) -> OrderOut:
    return OrderOut(
        id=order.id,
        status=order.status,
        total=order.total,
        created_at=order.created_at,
        items=[
            OrderItemOut(product_id=item.product_id, quantity=item.quantity, unit_price=item.unit_price)
            for item in order.items
        ],
    )


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    body: OrderIn,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> OrderOut:
    if idempotency_key is None or not idempotency_key.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Idempotency-Key is required")
    key = idempotency_key.strip()
    existing = await session.scalar(
        select(IdempotencyRecord).where(
            IdempotencyRecord.user_id == user.id,
            IdempotencyRecord.key == key,
        )
    )
    if existing is not None:
        stored = OrderOut.model_validate(json.loads(existing.body))
        return stored

    total = Decimal("0.00")
    pending: list[tuple[Product, int]] = []
    for item in body.items:
        product = await session.scalar(
            select(Product).where(Product.id == item.product_id).with_for_update()
        )
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Insufficient stock")
        product.stock -= item.quantity
        pending.append((product, item.quantity))
        total += product.price * item.quantity

    order = Order(user_id=user.id, status="submitted", total=total)
    session.add(order)
    await session.flush()
    for product, quantity in pending:
        session.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
            )
        )
    await session.flush()
    await session.refresh(order, attribute_names=["items", "created_at"])
    payload = _to_out(order)
    session.add(
        IdempotencyRecord(
            user_id=user.id,
            key=key,
            status_code=201,
            body=payload.model_dump_json(),
        )
    )
    return payload


@router.get("", response_model=list[OrderOut])
async def list_orders(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
) -> list[OrderOut]:
    result = await session.scalars(
        select(Order)
        .where(Order.user_id == user.id)
        .options(selectinload(Order.items))
        .order_by(Order.id)
    )
    return [_to_out(order) for order in result]


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
) -> OrderOut:
    order = await session.scalar(
        select(Order).where(Order.id == order_id).options(selectinload(Order.items))
    )
    if order is None or order.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return _to_out(order)

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.deps import require_admin
from app.models import Category, Product, User
from app.schemas import CategoryIn, CategoryOut, PageOut, ProductIn, ProductOut

router = APIRouter(tags=["catalog"])


@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    body: CategoryIn,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
) -> Category:
    existing = await session.scalar(select(Category).where(Category.name == body.name))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category exists")
    category = Category(name=body.name)
    session.add(category)
    await session.flush()
    return category


@router.get("/categories", response_model=list[CategoryOut])
async def list_categories(session: AsyncSession = Depends(get_session)) -> list[Category]:
    result = await session.scalars(select(Category).order_by(Category.id))
    return list(result)


@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    body: ProductIn,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
) -> Product:
    category = await session.get(Category, body.category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    product = Product(
        name=body.name,
        price=body.price,
        stock=body.stock,
        category_id=body.category_id,
    )
    session.add(product)
    await session.flush()
    return product


@router.get("/products", response_model=PageOut)
async def list_products(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    category_id: int | None = None,
    q: str | None = Query(default=None, max_length=200),
) -> PageOut:
    stmt = select(Product).order_by(Product.id)
    if category_id is not None:
        stmt = stmt.where(Product.category_id == category_id)
    if q:
        escaped = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        stmt = stmt.where(Product.name.ilike(f"%{escaped}%", escape="\\"))
    result = await session.scalars(stmt.limit(limit).offset(offset))
    items = [ProductOut.model_validate(row) for row in result]
    return PageOut(items=items, limit=limit, offset=offset)

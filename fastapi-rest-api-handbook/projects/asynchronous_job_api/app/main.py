import json
import uuid

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base, Job, engine, get_session, settings

app = FastAPI(title="Asynchronous Job API", version="0.1.0")
redis_client: Redis | None = None


class JobIn(BaseModel):
    task: str = Field(pattern=r"^[a-z0-9_]{1,40}$")
    value: int = Field(ge=0, le=10_000)
    idempotency_key: str | None = Field(default=None, max_length=200)


class JobOut(BaseModel):
    id: str
    status: str
    result: str | None
    error: str | None
    attempts: int


def to_out(job: Job) -> JobOut:
    return JobOut(id=job.id, status=job.status, result=job.result, error=job.error, attempts=job.attempts)


@app.on_event("startup")
async def startup() -> None:
    global redis_client
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    redis_client = Redis.from_url(settings.redis_url)


@app.on_event("shutdown")
async def shutdown() -> None:
    if redis_client is not None:
        await redis_client.aclose()
    await engine.dispose()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/worker")
async def worker_health(session: AsyncSession = Depends(get_session)) -> dict[str, int | str]:
    queued = await session.scalar(select(func.count()).select_from(Job).where(Job.status == "QUEUED"))
    return {"status": "ok", "queued": int(queued or 0)}


@app.post("/jobs", response_model=JobOut, status_code=status.HTTP_202_ACCEPTED)
async def submit_job(body: JobIn, session: AsyncSession = Depends(get_session)) -> JobOut:
    if body.idempotency_key:
        existing = await session.scalar(select(Job).where(Job.idempotency_key == body.idempotency_key))
        if existing is not None:
            return to_out(existing)
    job = Job(
        id=str(uuid.uuid4()),
        idempotency_key=body.idempotency_key,
        status="QUEUED",
        payload=json.dumps({"task": body.task, "value": body.value}),
        attempts=0,
    )
    session.add(job)
    await session.flush()
    if redis_client is None:
        raise HTTPException(status_code=503, detail="Queue unavailable")
    await redis_client.lpush("jobs", job.id)
    return to_out(job)


@app.get("/jobs/{job_id}", response_model=JobOut)
async def get_job(job_id: str, session: AsyncSession = Depends(get_session)) -> JobOut:
    job = await session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return to_out(job)


@app.post("/jobs/{job_id}/cancel", response_model=JobOut)
async def cancel_job(job_id: str, session: AsyncSession = Depends(get_session)) -> JobOut:
    job = await session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status in {"SUCCEEDED", "FAILED", "DEAD"}:
        raise HTTPException(status_code=409, detail="Job already finished")
    job.cancel_requested = True
    if job.status == "QUEUED":
        job.status = "CANCELLED"
    return to_out(job)

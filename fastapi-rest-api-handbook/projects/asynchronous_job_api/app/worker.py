"""Queue worker. Durable state lives in PostgreSQL. Redis only wakes the worker."""

import asyncio
import json
import logging

from redis.asyncio import Redis
from sqlalchemy import select

from app.db import Base, Job, SessionLocal, engine, settings

log = logging.getLogger("worker")
logging.basicConfig(level=logging.INFO)


async def process_one(redis: Redis) -> None:
    job_id = await redis.brpop(["jobs"], timeout=2)  # type: ignore[misc]
    if not job_id:
        return
    _, raw = job_id
    identifier = raw.decode() if isinstance(raw, bytes) else raw
    async with SessionLocal() as session:
        job = await session.scalar(select(Job).where(Job.id == identifier).with_for_update())
        if job is None or job.status != "QUEUED":
            await session.commit()
            return
        if job.cancel_requested:
            job.status = "CANCELLED"
            await session.commit()
            return
        job.status = "RUNNING"
        job.attempts += 1
        await session.commit()
        payload = json.loads(job.payload)
        try:
            if payload["task"] == "fail_once" and job.attempts < 2:
                raise RuntimeError("transient")
            if payload["task"] == "always_fail":
                raise RuntimeError("permanent")
            result = str(int(payload["value"]) * 2)
            error = None
            status = "SUCCEEDED"
        except Exception as exc:  # noqa: BLE001
            result = None
            error = str(exc)
            if job.attempts >= settings.max_attempts:
                status = "DEAD"
            else:
                status = "QUEUED"
        job = await session.scalar(select(Job).where(Job.id == identifier).with_for_update())
        if job is None:
            return
        if job.cancel_requested and status == "SUCCEEDED":
            job.status = "CANCELLED"
        else:
            job.status = status
            job.result = result
            job.error = error
        await session.commit()
        if job.status == "QUEUED":
            await redis.lpush("jobs", job.id)
            log.info("requeued %s attempt %s", job.id, job.attempts)


async def main() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    redis = Redis.from_url(settings.redis_url)
    log.info("worker started")
    try:
        while True:
            await process_one(redis)
    finally:
        await redis.aclose()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

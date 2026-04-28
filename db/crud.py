import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from db.models.scan import ScanTask, IntelligenceRecord, ThreatActor


# ── ScanTask ──────────────────────────────────────────────────────────────────

async def create_scan_task(db: AsyncSession, target: str) -> ScanTask:
    task = ScanTask(
        task_id=str(uuid.uuid4()),
        target=target,
        status="pending"
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_scan_task(db: AsyncSession, task_id: str) -> Optional[ScanTask]:
    result = await db.execute(select(ScanTask).where(ScanTask.task_id == task_id))
    return result.scalar_one_or_none()


async def update_scan_status(db: AsyncSession, task_id: str, status: str, **kwargs):
    values = {"status": status, "updated_at": datetime.utcnow(), **kwargs}
    await db.execute(
        update(ScanTask).where(ScanTask.task_id == task_id).values(**values)
    )
    await db.commit()


async def list_scan_tasks(db: AsyncSession, limit: int = 50) -> List[ScanTask]:
    result = await db.execute(
        select(ScanTask).order_by(ScanTask.created_at.desc()).limit(limit)
    )
    return result.scalars().all()


# ── IntelligenceRecord ────────────────────────────────────────────────────────

async def bulk_insert_records(db: AsyncSession, records: List[dict]):
    objs = [IntelligenceRecord(**r) for r in records]
    db.add_all(objs)
    await db.commit()


async def get_verified_records(db: AsyncSession, task_id: str) -> List[IntelligenceRecord]:
    result = await db.execute(
        select(IntelligenceRecord)
        .where(IntelligenceRecord.scan_task_id == task_id)
        .where(IntelligenceRecord.verified == True)
    )
    return result.scalars().all()


# ── ThreatActor ───────────────────────────────────────────────────────────────

async def upsert_threat_actor(db: AsyncSession, name: str, **kwargs) -> ThreatActor:
    result = await db.execute(select(ThreatActor).where(ThreatActor.name == name))
    actor = result.scalar_one_or_none()
    if actor:
        for k, v in kwargs.items():
            setattr(actor, k, v)
    else:
        actor = ThreatActor(name=name, **kwargs)
        db.add(actor)
    await db.commit()
    await db.refresh(actor)
    return actor

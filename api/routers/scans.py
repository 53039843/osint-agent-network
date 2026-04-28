from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from worker.tasks import run_pipeline_task
from utils.logger import setup_logger

logger = setup_logger("api_scans")
router = APIRouter(prefix="/api/v1/scans", tags=["Scans"])


class ScanRequest(BaseModel):
    target: str
    sources: Optional[List[str]] = None
    priority: Optional[str] = "normal"  # normal / high


class ScanResponse(BaseModel):
    task_id: str
    target: str
    status: str
    message: str


@router.post("/", response_model=ScanResponse, summary="Start a new OSINT scan")
async def create_scan(request: ScanRequest):
    """
    Submits a new OSINT analysis task to the Celery worker queue.
    Returns a task_id that can be used to poll for results.
    """
    if not request.target.strip():
        raise HTTPException(status_code=400, detail="Target cannot be empty")

    task = run_pipeline_task.delay(request.target)
    logger.info(f"Queued scan task {task.id} for target: {request.target}")

    return ScanResponse(
        task_id=task.id,
        target=request.target,
        status="queued",
        message="Scan task submitted to worker queue"
    )


@router.get("/{task_id}", summary="Get scan status and results")
async def get_scan(task_id: str):
    """
    Retrieves the current status and results of a scan task.
    """
    from celery.result import AsyncResult
    result = AsyncResult(task_id, app=run_pipeline_task.app)

    if result.state == "PENDING":
        return {"task_id": task_id, "status": "pending", "result": None}
    elif result.state == "STARTED":
        return {"task_id": task_id, "status": "running", "result": None}
    elif result.state == "SUCCESS":
        return {"task_id": task_id, "status": "completed", "result": result.result}
    elif result.state == "FAILURE":
        return {"task_id": task_id, "status": "failed", "error": str(result.result)}
    else:
        return {"task_id": task_id, "status": result.state, "result": None}


@router.get("/", summary="List recent scans")
async def list_scans(limit: int = 20):
    """Returns a list of recently submitted scan tasks."""
    # In production this would query the database
    return {"message": f"Returning last {limit} scans", "scans": []}

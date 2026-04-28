from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio

# Import main pipeline
from main import run_osint_pipeline

app = FastAPI(
    title="OSINT Agent Network API",
    description="REST API for the Multi-Agent OSINT analysis system.",
    version="0.1.0"
)

class AnalysisRequest(BaseModel):
    target: str
    sources: List[str] = ["twitter", "reddit"]

class AnalysisResponse(BaseModel):
    status: str
    message: str
    target: str

# In-memory store for task status (for demonstration)
tasks_status: Dict[str, str] = {}

async def execute_pipeline_background(target: str):
    tasks_status[target] = "running"
    try:
        await run_osint_pipeline(target)
        tasks_status[target] = "completed"
    except Exception as e:
        tasks_status[target] = f"failed: {str(e)}"

@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Starts an asynchronous OSINT analysis pipeline for the given target.
    """
    if request.target in tasks_status and tasks_status[request.target] == "running":
        return AnalysisResponse(status="error", message="Task already running", target=request.target)
        
    background_tasks.add_task(execute_pipeline_background, request.target)
    
    return AnalysisResponse(
        status="success", 
        message="Analysis pipeline started in background", 
        target=request.target
    )

@app.get("/api/v1/status/{target}")
async def get_status(target: str):
    """
    Checks the status of an ongoing analysis.
    """
    status = tasks_status.get(target, "not_found")
    return {"target": target, "status": status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

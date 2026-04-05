from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.worker import celery_app, run_autonomous_agent

router = APIRouter(prefix="/agents", tags=["agents"])

class AgentJobRequest(BaseModel):
    prompt: str

class AgentJobStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Any | None = None

@router.post("/start")
def start_agent_task(job_req: AgentJobRequest) -> AgentJobStatusResponse:
    task = run_autonomous_agent.delay(job_req.prompt)
    return AgentJobStatusResponse(
        task_id=task.id,
        status="Processing"
    )

@router.get("/status/{task_id}")
def get_agent_task_status(task_id: str) -> AgentJobStatusResponse:
    task_result = celery_app.AsyncResult(task_id)
    return AgentJobStatusResponse(
        task_id=task_id,
        status=task_result.status,
        result=task_result.result if task_result.ready() else None
    )

from uuid import uuid4

from app.schemas.analysis import AnalysisJob, IntakeRequest, JobEnqueueResponse


class InMemoryJobQueue:
    def __init__(self) -> None:
        self.jobs: dict[str, AnalysisJob] = {}

    def enqueue(self, payload: IntakeRequest) -> JobEnqueueResponse:
        job_id = str(uuid4())
        job = AnalysisJob(
            job_id=job_id,
            account_role=payload.account_role,
            documents=payload.documents,
            status="queued"
        )
        self.jobs[job_id] = job
        return JobEnqueueResponse(job_id=job_id, status=job.status)

    def get(self, job_id: str) -> AnalysisJob | None:
        return self.jobs.get(job_id)

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.analysis import router as analysis_router
from app.api.routes.health import router as health_router
from app.config import settings
from app.governance.constraints import GovernanceRefusal

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Standalone COI review API for contract-to-certificate comparison and endorsement request drafting."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(health_router)
app.include_router(analysis_router, prefix="/api")


@app.exception_handler(GovernanceRefusal)
async def governance_refusal_handler(_, exc: GovernanceRefusal) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": "governance_refusal",
            "reason": exc.reason,
            "detail": exc.detail,
        }
    )

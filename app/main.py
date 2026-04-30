from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as api_router
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("propintel-api")

app = FastAPI(
    title="PropIntel AI Copilot",
    description="NBFC-Grade Collateral Evaluation & Risk Intelligence",
    version="2.0.0"
)

# CORS configuration for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for request tracking and audit logging
@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Audit log entry
    logger.info(
        f"Path: {request.url.path} | "
        f"Method: {request.method} | "
        f"Status: {response.status_code} | "
        f"Duration: {duration:.4f}s"
    )
    return response

# Include routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "PropIntel AI Copilot", "version": "2.0.0"}

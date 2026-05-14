import uvicorn
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
# Force reload
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.db import models_registry # Ensure all models are registered on Base

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan — runs startup logic before serving requests.
    Mistral model initialisation is optional and non-blocking.
    Set DISABLE_MISTRAL=1 to skip model loading (lightweight deployments).
    """
    if os.getenv("DISABLE_MISTRAL", "0") != "1":
        try:
            from app.ai.mistral_multi_adapter_service import mistral_service
            logger.info("Attempting to initialise Mistral multi-adapter service...")
            success = mistral_service.initialize()
            if success:
                logger.info("✓ Mistral-7B loaded and ready.")
            else:
                logger.info("Mistral unavailable — running on Gemini/G4F/fallback.")
        except Exception as e:
            logger.warning(f"Mistral startup skipped: {e}")
    else:
        logger.info("DISABLE_MISTRAL=1 — skipping Mistral model load.")

    yield  # Application runs here

    # Shutdown: nothing to clean up for quantised model
    logger.info("Fuelix API shutting down.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080", "http://localhost:3000", "http://127.0.0.1:8080", "http://127.0.0.1:3000", "*"],
        allow_credentials=False, # Must be False if origins has "*"
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to Fuelix Hybrid Athlete API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

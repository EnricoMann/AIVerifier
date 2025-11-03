from fastapi import APIRouter
from app.api import factcheck, ollama_ai
from app.api import history

router = APIRouter()
router.include_router(factcheck.router, tags=["factcheck"])
router.include_router(ollama_ai.router, tags=["ollama"])
router.include_router(history.router)
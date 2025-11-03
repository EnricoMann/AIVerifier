from fastapi import APIRouter, HTTPException
from app.api.factcheck_aggregator import aggregate_factchecks

router = APIRouter()

@router.post("/verify")
async def verify(payload: dict):
    query = payload.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Missing 'query'")

    sources = await aggregate_factchecks(query)
    return {"claim": query, "sources": sources}

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from src.pipeline import condense_condolences
from src.pydantic_class import CondenseResult, CondolencesRequest

app = FastAPI(
    title="Tribute Lens – Condolence Condenser API",
    version="0.1.0",
    description="AI-only layer: takes condolence messages → returns overview, keywords, highlighted quote.",
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/condense", response_model=CondenseResult)
async def condense(req: CondolencesRequest) -> CondenseResult:
    result = condense_condolences(req.messages, req.old_result)
    return CondenseResult(
        overview=result.overview,
        memory_keywords=result.memory_keywords,
        highlighted_quote=result.highlighted_quote,
        memory_cloud_data=result.memory_cloud_data
    )

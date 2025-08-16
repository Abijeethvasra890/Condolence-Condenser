from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from src.pipeline import condense_condolences

app = FastAPI(
    title="Tribute Lens – Condolence Condenser API",
    version="0.1.0",
    description="AI-only layer: takes condolence messages → returns overview, keywords, highlighted quote.",
)

class CondolencesRequest(BaseModel):
    messages: List[str] = Field(..., description="Array of condolence messages for a single obituary/person.")

class CondenseResponse(BaseModel):
    overview: str
    memory_keywords: List[str]
    highlighted_quote: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/condense", response_model=CondenseResponse)
async def condense(req: CondolencesRequest) -> CondenseResponse:
    result = condense_condolences(req.messages)
    return CondenseResponse(
        overview=result.overview,
        memory_keywords=result.memory_keywords,
        highlighted_quote=result.highlighted_quote,
    )

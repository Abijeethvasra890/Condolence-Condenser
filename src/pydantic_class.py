import json
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class WordCloudItem(BaseModel):
    word: str = Field(..., description="The word to display in the memory cloud")
    frequency: int = Field(..., description="The frequency count of the word")

class CondenseResult(BaseModel):
    overview: str = Field(..., description="Short, heartfelt paragraph capturing collective sentiment.")
    memory_keywords: List[str] = Field(..., description="5–7 short keywords/phrases (1–3 words).")
    highlighted_quote: str = Field(..., description="One verbatim line from the input messages.")
    memory_cloud_data: List[WordCloudItem] = Field(
        ...,
        description="Array of word-frequency pairs for word cloud data."
    )

class CondolencesRequest(BaseModel):
    messages: List[str] = Field(..., description="Array of condolence messages for a single obituary/person.")

    old_result: Optional[CondenseResult] = Field(
        None,
        description="Optional previously generated structured condolence data. "
                    "If provided, the AI will merge this with the new condolence(s)."
    )
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from src.llm import get_llm
from src.filters import clean_and_filter
from src.prompts import PROMPT

class CondenseResult(BaseModel):
    overview: str = Field(..., description="Short, heartfelt paragraph capturing collective sentiment.")
    memory_keywords: List[str] = Field(..., description="5-7 short keywords/phrases (1–3 words).")
    highlighted_quote: str = Field(..., description="One verbatim line from the input messages.")

def build_chain():
    base_parser = PydanticOutputParser(pydantic_object=CondenseResult)
    # Try to auto-fix minor JSON issues if model drifts
    fixing_parser = OutputFixingParser.from_llm(parser=base_parser, llm=get_llm(temperature=0))
    prompt = PROMPT.partial(format_instructions=base_parser.get_format_instructions())

    chain = (
        {"messages_json": RunnablePassthrough()}
        | prompt
        | get_llm(temperature=0.2)
        | fixing_parser
    )
    return chain

_chain = build_chain()

def condense_condolences(messages: List[str]) -> CondenseResult:
    """
    1) Filter generic/short messages (RIP, emojis, etc.).
    2) Ask the LLM for structured JSON with:
       - overview
       - memory_keywords
       - highlighted_quote (verbatim from inputs)
    """
    filtered = clean_and_filter(messages)
    if not filtered:
        # Fallback: if everything got filtered, use originals (still safer)
        filtered = [m for m in messages if m and m.strip()]

    # Keep payload compact but representative (optional: cap to first 200)
    payload = json.dumps(filtered[:200], ensure_ascii=False)

    result: CondenseResult = _chain.invoke(payload)
    # Post-process: trim keywords, ensure uniqueness
    seen = set()
    cleaned_kw = []
    for w in result.memory_keywords:
        w2 = " ".join(w.strip().split())
        if not w2:
            continue
        low = w2.lower()
        if low not in seen:
            seen.add(low)
            cleaned_kw.append(w2)
    # keep 5–7 only
    cleaned_kw = cleaned_kw[:7]
    return CondenseResult(
        overview=result.overview.strip(),
        memory_keywords=cleaned_kw,
        highlighted_quote=result.highlighted_quote.strip().strip('"'),
    )

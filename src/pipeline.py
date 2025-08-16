import json
from typing import List, Optional
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.schema.runnable import RunnablePassthrough
from src.llm import get_llm
from src.filters import clean_and_filter
from src.prompts import PROMPT
from src.pydantic_class import CondenseResult


def build_chain():
    base_parser = PydanticOutputParser(pydantic_object=CondenseResult)
    fixing_parser = OutputFixingParser.from_llm(
        parser=base_parser, llm=get_llm(temperature=0)
    )
    # inject format instructions into the prompt template
    prompt = PROMPT.partial(format_instructions=base_parser.get_format_instructions())

    # Provide two named runnables so the prompt receives both fields
    chain = (
        {
            "new_messages": RunnablePassthrough(),
            "previous_structured_data": RunnablePassthrough(),
        }
        | prompt
        | get_llm(temperature=0.2)
        | fixing_parser
    )
    return chain


_chain = build_chain()


def condense_condolences(
    messages: List[str], old_result: Optional[CondenseResult] = None
) -> CondenseResult:
    """
    Condense condolence messages. If old_result is provided, pass it as previous_structured_data
    so the LLM merges old + new and returns updated structured output.
    """
    filtered = clean_and_filter(messages)
    if not filtered:
        filtered = [m for m in messages if m and m.strip()]

    # prepare JSON strings for stable formatting inside the prompt
    new_messages_json = filtered[:200]  # keep as list
    prev_json = old_result.model_dump() if old_result else None

    result: CondenseResult = _chain.invoke({
        "new_messages": new_messages_json,
        "previous_structured_data": prev_json,
    })


    # Post-process keywords (dedup, cleanup, cap to 7)
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
    cleaned_kw = cleaned_kw[:7]

    return CondenseResult(
        overview=result.overview.strip(),
        memory_keywords=cleaned_kw,
        highlighted_quote=result.highlighted_quote.strip().strip('"'),
        memory_cloud_data=result.memory_cloud_data or [],
    )

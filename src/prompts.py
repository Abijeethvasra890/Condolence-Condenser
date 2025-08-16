from langchain.prompts import ChatPromptTemplate

SYSTEM_PROMPT = (
    "You are a compassionate assistant helping to reflect the essence of condolence messages. "
    "Preserve human sentiment, avoid clichés, and DO NOT invent facts or names. "
    "You must return STRICT JSON only."
)

# We’ll inject {messages_json} and {format_instructions}
PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "user",
            (
                "Here is a JSON array of condolence messages for one person:\n\n"
                "{messages_json}\n\n"
                "Tasks:\n"
                "1) You are given several condolence messages. Write one condensed condolence message that preserves the emotions, empathy," 
                "and respect from all messages. Do not explain or analyze. Write it as if you are personally expressing condolences.\n"
                "2) From the given condolence messages, extract the most important keywords and short phrases that capture emotions, "
                "memories, and values. Keep them brief, under 3 words each.\n"
                "3) Return ONE HIGHLIGHTED QUOTE: choose a single touching line VERBATIM from the input messages "
                "(do not paraphrase; if a message has multiple sentences, pick the most impactful sentence). "
                "Prefer quotes that are specific and personal over generic condolences.\n\n"
                "{format_instructions}"
            ),
        ),
    ]
)

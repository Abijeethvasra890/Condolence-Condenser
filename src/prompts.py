# from langchain.prompts import ChatPromptTemplate

# SYSTEM_PROMPT = (
#     "You are a compassionate assistant helping to reflect the essence of condolence messages. "
#     "Preserve human sentiment, avoid clichés, and DO NOT invent facts or names. "
#     "You must return STRICT JSON only."
# )

# # We’ll inject {messages_json} and {format_instructions}
# PROMPT = ChatPromptTemplate.from_messages(
#     [
#         ("system", SYSTEM_PROMPT),
#         (
#             "user",
#             (
#                 "Here is a JSON array of condolence messages for one person:\n\n"
#                 "{messages_json}\n\n"
#                 "Tasks:\n"
#                 "1) You are given several condolence messages. Write one condensed condolence message that preserves the emotions, empathy," 
#                 "and respect from all messages. Do not explain or analyze. Write it as if you are personally expressing condolences.\n"
#                 "2) From the given condolence messages, extract the most important keywords and short phrases that capture emotions, "
#                 "memories, and values. Keep them brief, under 3 words each.\n"
#                 "3) Return ONE HIGHLIGHTED QUOTE: choose a single touching line VERBATIM from the input messages "
#                 "(do not paraphrase; if a message has multiple sentences, pick the most impactful sentence). "
#                 "Prefer quotes that are specific and personal over generic condolences.\n\n"
#                 "{format_instructions}"
#             ),
#         ),
#     ]
# )

from langchain.prompts import ChatPromptTemplate

# SYSTEM_PROMPT = (
#     "You are a compassionate assistant who helps express the collective voice of condolence messages. "
#     "Your task is to preserve *human sentiment* and *emotional authenticity*. "
#     "Do NOT produce summaries, analysis, or meta-language. "
#     "Write the overview as if YOU are offering heartfelt condolences on behalf of the group. "
#     "Do NOT invent names or facts. Only use the words and emotions present in the messages."
# )

# PROMPT = ChatPromptTemplate.from_messages(
#     [
#         ("system", SYSTEM_PROMPT),
#         (
#             "user",
#             (
#                 "You are given a JSON array of condolence messages for ONE deceased person:\n\n"
#                 "{messages_json}\n\n"
#                 "Perform these tasks and return STRICT JSON:\n\n"
#                 "1) overview → Write ONE heartfelt condolence message that blends the emotions and respect "
#                 "from all the inputs. It should sound personal, compassionate, and natural — "
#                 "as if you are expressing condolences yourself, not summarizing or analyzing.\n\n"
#                 "2) memory_keywords → Extract the most meaningful keywords or short phrases "
#                 "(1–3 words each) that reflect values, traits, or emotions from the messages.\n\n"
#                 "3) highlighted_quote → Select ONE powerful line VERBATIM from the input messages "
#                 "(not paraphrased). Prefer specific, emotional, and personal lines over generic ones.\n\n"
#                 "4) memoryCloudData → Return an array of objects with 'word' and 'frequency' keys. "
#                 "Count how many times each meaningful word/phrase appears across the messages. "
#                 "Keep them under 3 words, lowercase unless proper noun.\n\n"
#                 "{format_instructions}"
#             ),
#         ),
#     ]
# )

# SYSTEM_PROMPT = (
#     "You are a compassionate assistant who helps express the collective voice of condolence messages. "
#     "Your task is to preserve *human sentiment* and *emotional authenticity*. "
#     "Do NOT produce summaries, analysis, or meta-language. "
#     "Write the overview as if YOU are offering heartfelt condolences on behalf of the group. "
#     "Do NOT invent names or facts. Only use the words and emotions present in the messages."
# )

# PROMPT = ChatPromptTemplate.from_messages(
#     [
#         ("system", SYSTEM_PROMPT),
#         (
#             "user",
#             (
#                 "You are given condolence data for ONE deceased person in JSON format.\n\n"
#                 "{messages_json}\n\n"
#                 "If 'previous_structured_data' is present then add, it contains an earlier AI-generated result. "
#                 "Merge it with the new_messages instead of starting from scratch.\n\n"
#                 "Perform these tasks and return STRICT JSON:\n\n"
#                 "1) overview → Write ONE heartfelt condolence message that blends both old and new emotions. "
#                 "It should sound personal, compassionate, and natural — not like a summary.\n\n"
#                 "2) memory_keywords → Extract the most meaningful keywords/phrases (1–3 words each) "
#                 "covering both old and new messages.\n\n"
#                 "3) highlighted_quote → Select ONE powerful verbatim line from ANY input message. "
#                 "Prefer specific, emotional lines.\n\n"
#                 "4) memory_cloud_data → Return an array of objects with 'word' and 'frequency'. "
#                 "Count across both old and new messages.\n\n"
#                 "{format_instructions}"
#             ),
#         ),
#     ]
# )


from langchain.prompts import ChatPromptTemplate

SYSTEM_PROMPT = (
    "You are a compassionate assistant who helps express the collective voice of condolence messages. "
    "Your task is to preserve *human sentiment* and *emotional authenticity*. "
    "Do NOT produce summaries, analysis, or meta-language. "
    "Write the overview as if YOU are offering heartfelt condolences on behalf of the group. "
    "Do NOT invent names or facts. Only use the words and emotions present in the messages."
)

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "user",
            (
                "You are given condolence data for ONE deceased person in JSON format.\n\n"
                "{new_messages}\n\n"
                "If 'previous_structured_data' is present, it contains an earlier AI-generated result.\n"
                "Merge it with the new_messages instead of starting from scratch.\n\n"
                "Perform these tasks and return STRICT JSON:\n\n"
                "1) overview → Write ONE heartfelt condolence message that blends both old and new emotions. "
                "It should sound personal, compassionate, and natural — not like a summary.\n\n"
                "2) memory_keywords → Extract the most meaningful keywords/phrases (1–3 words each) "
                "covering both old and new messages.\n\n"
                "3) highlighted_quote → Select ONE powerful verbatim line from ANY input message. "
                "Prefer specific, emotional lines.\n\n"
                "4) memory_cloud_data → Return an array of objects with 'word' and 'frequency'. "
                "Count across both old and new messages.\n\n"
                "{format_instructions}"
            ),
        ),
    ]
)

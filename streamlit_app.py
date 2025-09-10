import json
from typing import Optional, List, Any
import html
from wordcloud import WordCloud
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

import streamlit as st

from src.pipeline import condense_condolences
from src.pydantic_class import CondenseResult

# ---------- Page config ----------
st.set_page_config(page_title="Tribute Lens — Demo", layout="wide", page_icon="🕊️")

# ---------- Helper functions ----------
def parse_messages_input(text: str) -> Optional[List[str]]:
    """Parse a JSON array of strings (messages)."""
    try:
        data = json.loads(text)
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data
        # attempt to accept newline-separated text (fallback)
        if isinstance(data, str):
            return [line.strip() for line in data.splitlines() if line.strip()]
    except Exception:
        # try as newline separated plain text
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if lines:
            return lines
    return None

def parse_old_result(text: str) -> Optional[CondenseResult]:
    """Try to parse old_result JSON into CondenseResult safely."""
    if not text:
        return None
    try:
        # pydantic v2
        if hasattr(CondenseResult, "model_validate_json"):
            return CondenseResult.model_validate_json(text)
        # pydantic v1
        return CondenseResult.parse_raw(text)
    except Exception:
        try:
            data = json.loads(text)
            return CondenseResult(**data)
        except Exception:
            return None

def render_keywords_chips(keywords: List[str]):
    chips_html = "<div style='display:flex;flex-wrap:wrap;gap:8px;'>"
    for k in keywords:
        chips_html += (
            f"<div style='padding:6px 10px;border-radius:999px;background:#f1f5f9;"
            f"border:1px solid #e2e8f0;font-weight:600;font-size:0.95rem'>{html.escape(k)}</div>"
        )
    chips_html += "</div>"
    st.markdown(chips_html, unsafe_allow_html=True)

def render_quote_box(quote: str):
    st.markdown(
        f"""
        <div style="border-left:4px solid #94a3b8;padding:12px 16px;background:#fbfbfd;border-radius:8px;">
            <p style="margin:0;font-style:italic;color:#0f172a;">“{html.escape(quote)}”</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_memory_cloud(memory_cloud: list):
    """
    Render a word cloud image based on memory_cloud data.
    Accepts memory_cloud as list of {"word": str, "frequency": int} OR
    pydantic model objects with `.word` and `.frequency` attributes.
    """
    if not memory_cloud:
        st.info("No memory cloud data available.")
        return

    items = []
    for it in memory_cloud:
        # handle dict-like items
        if isinstance(it, dict):
            word = it.get("word") or it.get("text") or it.get("label")
            freq = it.get("frequency") or it.get("freq") or it.get("count")
        else:
            # handle pydantic model or arbitrary object
            word = getattr(it, "word", None) or getattr(it, "text", None) or getattr(it, "label", None)
            freq = getattr(it, "frequency", None) or getattr(it, "freq", None) or getattr(it, "count", None)

        if not word:
            continue

        # Clean and coerce
        word_str = str(word).strip()
        try:
            freq_int = int(freq) if freq is not None else 1
            if freq_int < 0:
                freq_int = abs(freq_int)
        except Exception:
            freq_int = 1

        if word_str:
            items.append({"word": word_str, "frequency": freq_int})

    if not items:
        st.info("No valid words to render in cloud.")
        return

    # Build frequency dict for WordCloud
    freq_dict = {it["word"]: it["frequency"] for it in items}

    wc = WordCloud(
        width=400,
        height=200,
        background_color="ivory",
        colormap="magma",
        prefer_horizontal=0.7,
        collocations=False,
        min_font_size=5,
        max_font_size=50,
        contour_color="steelblue",
        contour_width=1,
        relative_scaling=0.5,
    ).generate_from_frequencies(freq_dict)

    # Control display size
    # Convert to PIL image
    img = wc.to_image()

    # Resize explicitly (e.g., half size)
    img_resized = img.resize((800, 450))  # (width, height) in pixels

    # Now Streamlit will honor this size
    st.image(img_resized, caption="Memory Cloud")

# ---------- UI ----------
st.markdown("# Tribute Lens — Condolence Condenser")
st.markdown(
    "Paste an array of condolence messages (JSON array) below. Optionally paste previous `CondenseResult` JSON "
    "if available (the AI will merge old + new)."
)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Input — New Condolences")
    messages_input = st.text_area(
        "Messages (JSON array of strings) or plain newline-separated messages",
        height=300,
        value=json.dumps(
            [
                  "John was always there for us — the first to help, the last to leave.",
                    "I'll never forget his laughter on summer evenings by the lake.",
                    "He taught me patience and kindness just by the way he lived.",
                    "Our church will miss his gentle advice and warm smile.",
                    "I loved his Sunday pancakes; he made them for everyone without fail.",
                    "John inspired me to volunteer; he believed in giving more than taking.",
            ],
            ensure_ascii=False,
            indent=2,
        ),
    )

    st.subheader("Optional — Previous CondenseResult (JSON)")
    old_result_input = st.text_area(
        "Paste previous CondenseResult JSON here (optional). Leave empty to create a fresh result.",
        height=200,
        placeholder='{"overview":"...","memory_keywords":["..."],"highlighted_quote":"...","memory_cloud_data":[{"word":"...","frequency":1}]}',
    )

    run = st.button("✨ Generate Condensed Tribute")

with col2:
    st.markdown("### Controls")
    st.write("- `old_result` optional: if provided, pipeline will attempt merge.")
    st.write("- The pipeline uses your server-side LLM settings (Groq).")
    st.write("")
    st.markdown("### Quick actions")
    if st.button("Load sample old_result"):
        sample_old = {
            "overview": "Anil was a loving teacher and community pillar.",
            "memory_keywords": ["kindness", "teaching", "community"],
            "highlighted_quote": "Mr. Anil Sharma guided me through physics at Greenwood High with so much patience.",
            "memory_cloud_data": [
                {"word": "kindness", "frequency": 4},
                {"word": "community", "frequency": 3},
                {"word": "teaching", "frequency": 3},
            ],
        }
        old_result_input = json.dumps(sample_old, ensure_ascii=False, indent=2)
        st.experimental_set_query_params() 
        st.success("Sample shown below — paste it into the 'Previous CondenseResult' field.")

# ---------- Run pipeline ----------
result: Optional[CondenseResult] = None
if run:
    msgs = parse_messages_input(messages_input or "")
    if not msgs:
        st.error("Could not parse messages. Provide a JSON array of strings or newline-separated messages.")
    else:
        old_model = parse_old_result(old_result_input or "")
        with st.spinner("Calling pipeline... (LLM may take a few seconds)"):
            try:
                # call your pipeline directly
                result = condense_condolences(msgs, old_model)
            except Exception as e:
                st.exception(e)

# ---------- Output area ----------
st.markdown("---")
out_col1, out_col2 = st.columns([3, 1])

with out_col1:
    st.subheader("AI Output")
    if result:
        st.markdown("#### Overview")
        st.markdown(f"<div style='font-size:1.05rem;padding:8px 10px;background:#fff8f0;border-radius:8px;'>{html.escape(result.overview)}</div>", unsafe_allow_html=True)

        st.markdown("#### Memory Keywords")
        if result.memory_keywords:
            render_keywords_chips(result.memory_keywords)
        else:
            st.write("_No keywords provided._")

        st.markdown("#### Highlighted Quote")
        if result.highlighted_quote:
            render_quote_box(result.highlighted_quote)
        else:
            st.write("_No highlighted quote provided._")

        st.markdown("#### Memory Cloud")
        render_memory_cloud(result.memory_cloud_data)
    else:
        st.info("No AI output yet. Click **Generate Condensed Tribute** to run the pipeline.")

with out_col2:
    st.subheader("Raw JSON (AI response)")
    if result:
        st.json(result.model_dump())
    else:
        st.write("Will show the raw JSON output here after generation.")

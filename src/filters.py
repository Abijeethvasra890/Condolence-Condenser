import re
from typing import List

_GENERIC_PATTERNS = [
    r"^\s*r\.?i\.?p\.?\s*$",
    r"^\s*rest in peace.*$",
    r"^\s*my condolences\.?\s*$",
    r"^\s*condolences\.?\s*$",
    r"^\s*🙏+\s*$",
    r"^\s*💐+\s*$",
    r"^\s*om shanti.*$",
    r"^\s*sorry for your loss\.?\s*$",
]
_GENERIC_RE = [re.compile(pat, re.IGNORECASE) for pat in _GENERIC_PATTERNS]

def is_generic(msg: str) -> bool:
    txt = msg.strip()
    if len(txt) < 8:
        return True
    for rx in _GENERIC_RE:
        if rx.match(txt):
            return True
    # mostly emojis/punctuation?
    if len(re.sub(r"[^\w]+", "", txt)) < 3:
        return True
    return False

def clean_and_filter(messages: List[str]) -> List[str]:
    seen = set()
    out = []
    for m in messages:
        if not m:
            continue
        m2 = re.sub(r"\s+", " ", m).strip()
        if is_generic(m2):
            continue
        if m2.lower() in seen:
            continue
        seen.add(m2.lower())
        out.append(m2)
    return out

import os
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None


DEFAULT_KEYWORDS = [
    "payments",
    "payment",
    "project management",
    "program management",
    "fintech",
    "stakeholder management",
    "delivery management",
    "digital transformation",
    "merchant services",
    "governance",
    "compliance",
    "product management",
]


def resolve_resume_path(resume_path: str | None = None) -> str | None:
    path = resume_path or os.getenv("RESUME_PATH") or "Chirag"
    if not path:
        return None

    if os.path.exists(path):
        return path

    if os.path.splitext(path)[1] == "":
        for ext in [".pdf", ".docx", ".doc", ".txt"]:
            candidate = f"{path}{ext}"
            if os.path.exists(candidate):
                return candidate

    return path

KEYWORD_ALIASES = {
    "project management": ["project management", "project manager"],
    "program management": ["program management", "program manager"],
    "product management": ["product management", "product manager"],
    "stakeholder management": ["stakeholder management", "stakeholder engagement"],
    "delivery management": ["delivery management", "delivery lead", "delivery manager"],
    "digital transformation": ["digital transformation", "transformation", "digital initiatives"],
    "merchant services": ["merchant services", "merchant acquiring"],
    "payments": ["payments", "payment", "payment gateway", "payment systems"],
}


def _normalize_keyword(keyword: str) -> str:
    return re.sub(r"\s+", " ", keyword.strip().lower())


def _match_keyword(text: str, keyword: str) -> bool:
    norm_text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    aliases = KEYWORD_ALIASES.get(keyword, [keyword])
    for alias in aliases:
        norm_alias = re.sub(r"[^a-z0-9]+", " ", alias.lower())
        if norm_alias in norm_text:
            return True
    return False


def extract_resume_keywords(resume_text: str) -> list[str]:
    text = resume_text or ""
    found = []
    for keyword in DEFAULT_KEYWORDS:
        if _match_keyword(text, keyword):
            found.append(keyword)

    if not found:
        return DEFAULT_KEYWORDS[:4]

    return found


def extract_experience_years(resume_text: str) -> int:
    text = resume_text or ""
    match = re.search(r"(\d{1,2})\s*\+?\s*years?", text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    return 12


def read_resume_text(resume_path: str | None = None) -> str:
    path = resolve_resume_path(resume_path)
    if not path or not os.path.exists(path):
        return ""

    if PdfReader is None:
        return ""

    try:
        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)
    except Exception:
        return ""


def build_job_search_queries(keywords: list[str] | None = None, location: str = "Bangalore") -> list[str]:
    selected = keywords or DEFAULT_KEYWORDS
    normalized = [_normalize_keyword(k) for k in selected if _normalize_keyword(k)]

    queries = []
    for keyword in normalized:
        if "payments" in keyword:
            queries.append(f"{keyword.title()} Project Manager")
            queries.append(f"{keyword.title()} Domain Expert")
        elif "project management" in keyword:
            queries.append("Project Manager Payments")
            queries.append("Program Manager Payments")
        elif "fintech" in keyword:
            queries.append("Fintech Project Manager")
            queries.append("Fintech Program Manager")

    if not queries:
        queries = [
            "Payments Project Manager",
            "Payments Domain Expert",
            "Fintech Project Manager",
        ]

    if location:
        return [f"{q} in {location}" for q in queries]

    return queries

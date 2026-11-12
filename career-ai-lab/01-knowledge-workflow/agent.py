"""A deterministic, permission-aware retrieval starter; no LLM is used."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Document:
    doc_id: str
    text: str
    allowed_roles: frozenset[str]


DOCS = (
    Document(
        "DOC-101",
        "Invoice questions are reviewed by the finance team. Record the invoice reference before escalating.",
        frozenset({"analyst"}),
    ),
    Document(
        "DOC-102",
        "Request access via the service desk. Access requests require manager approval.",
        frozenset({"staff", "analyst"}),
    ),
    Document(
        "DOC-103",
        "Report unusual processing failures to the operations team and attach the event identifier.",
        frozenset({"staff", "analyst"}),
    ),
)
STOPWORDS = {"a", "an", "and", "are", "by", "for", "how", "i", "is", "my", "of", "the", "to", "what", "who"}


def words(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower())) - STOPWORDS


def answer_with_sources(question: str, role: str, documents=DOCS, limit: int = 2) -> dict:
    """Return evidence only from documents authorized for this role."""
    if role not in {"staff", "analyst"}:
        raise ValueError("Unsupported role")
    if limit < 1:
        raise ValueError("limit must be positive")
    query_terms = words(question)
    if not query_terms:
        return {"status": "insufficient_evidence", "answer": None, "citations": []}
    matches = []
    for doc in documents:
        if role not in doc.allowed_roles:
            continue  # Authorization happens before any ranking or output.
        score = len(query_terms & words(doc.text))
        if score:
            matches.append((score, doc.doc_id, doc))
    matches.sort(key=lambda item: (-item[0], item[1]))
    chosen = [item[2] for item in matches[:limit]]
    if not chosen:
        return {"status": "insufficient_evidence", "answer": None, "citations": []}
    return {
        "status": "evidence_found",
        "answer": " ".join(doc.text for doc in chosen),
        "citations": [doc.doc_id for doc in chosen],
    }


if __name__ == "__main__":
    for role in ("staff", "analyst"):
        print(role, answer_with_sources("How should I handle an invoice question?", role))

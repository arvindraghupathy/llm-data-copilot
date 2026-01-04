ANALYTICAL_KEYWORDS = [
    "top", "highest", "lowest",
    "average", "sum", "count",
    "rank", "most", "least"
]

def is_analytical(question: str) -> bool:
    q = question.lower()
    return any(k in q for k in ANALYTICAL_KEYWORDS)

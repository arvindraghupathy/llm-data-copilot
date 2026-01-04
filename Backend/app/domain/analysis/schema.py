from collections import defaultdict
from typing import List, Dict, Any

def infer_schema(rows: List[dict]) -> Dict[str, list]:
    schema = defaultdict(set)

    for row in rows[:50]:  # sample
        for k, v in row.items():
            if v is not None:
                schema[k].add(type(v).__name__)

    return {k: list(v) for k, v in schema.items()}

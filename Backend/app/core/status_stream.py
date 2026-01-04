# app/core/status_stream.py
from collections import defaultdict
import asyncio
from typing import Dict, List

# Per-dataset subscribers
dataset_subscribers: Dict[str, List[asyncio.Queue]] = defaultdict(list)

# Global subscribers (landing page)
global_subscribers: List[asyncio.Queue] = []


def subscribe_dataset(dataset_id: str) -> asyncio.Queue:
    q = asyncio.Queue()
    dataset_subscribers[dataset_id].append(q)
    return q


def subscribe_global() -> asyncio.Queue:
    q = asyncio.Queue()
    global_subscribers.append(q)
    return q


def publish_dataset_status(dataset_id: str, status: str):
    event = {
        "type": "dataset_status",
        "dataset_id": dataset_id,
        "status": status,
    }

    # Notify dataset-specific subscribers
    for q in dataset_subscribers.get(dataset_id, []):
        q.put_nowait(event)

    # Notify global subscribers
    for q in global_subscribers:
        q.put_nowait(event)

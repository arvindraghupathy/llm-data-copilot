from abc import ABC, abstractmethod

class VectorStore(ABC):
    @abstractmethod
    def upsert(self, *, id: str, vector: list[float], payload: dict):
        pass

    @abstractmethod
    def query(self, *, vector: list[float], filters: dict, limit: int):
        pass

from typing import Any, Protocol


class Cache(Protocol):
    def get(self, key: str) -> Any | None:
        pass

    def set(self, key: str, value: Any, *, expire: int) -> None:
        pass

    def delete(self, key: str) -> None:
        pass

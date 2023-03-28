from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Optional


class Recorder(metaclass=ABCMeta):
    def __init__(
        self, project: str, run: Optional[str] = None, config: dict[str, Any] = {}
    ) -> None:
        pass

    @abstractmethod
    def log(self, content: Any, step: int, **kwargs: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def close(self) -> Any:
        raise NotImplementedError()

from __future__ import annotations

from typing import Any, ClassVar


class ModelRegistry:
    REGISTRY: ClassVar[dict[str, Any]] = {}

    @classmethod
    def models(cls) -> dict[str, Any]:
        return dict(cls.REGISTRY)

    @classmethod
    def register(cls, model_cls: Any) -> Any:
        name: str = model_cls.__name__
        cls.REGISTRY[name] = model_cls
        return model_cls

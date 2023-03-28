from __future__ import annotations

from typing import Any, Optional

from .recorder import Recorder

__all__ = ["Recorder", "recorder_factory"]


def recorder_factory(
    backend: str, project: str, run: Optional[str] = None, config: dict[str, Any] = {}
) -> Any:
    if backend == "wandb":
        import recorders.wandb_recorder

        return recorders.wandb_recorder.WandbRecorder(project, run=run, config=config)
    else:
        raise NotImplementedError("{} is not supported".format(backend))

from __future__ import annotations

from typing import Any, Optional

import wandb
from recorders import Recorder


class WandbRecorder(Recorder):  # type: ignore
    def __init__(
        self, project: str, run: Optional[str] = None, config: dict[str, Any] = {}
    ) -> None:
        super(WandbRecorder, self).__init__(project, run, config)
        wandb.init(project, name=run, config=config)

    def log(self, content: Any, step: int, **kwargs: Any) -> Any:
        return wandb.log(content, step, **kwargs)

    def close(self) -> Any:
        return wandb.finish()

from typing import Any

import torch
import torch.nn as nn

from .utils import ModelRegistry


@ModelRegistry.register
class MLP(nn.Module):
    def __init__(
        self,
        *,
        in_dim: int,
        hidden_dim: int,
        out_dim: int,
        dropout: float = 0.5,
        **kwargs: Any
    ) -> None:
        super(MLP, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(p=dropout),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(self, x: torch.Tensor) -> Any:
        return self.layers(x)

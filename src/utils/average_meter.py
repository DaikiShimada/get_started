from typing import Optional


class AverageMeter:
    _val: float
    _avg: Optional[float]
    _sum: float
    _count: int

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._val = 0
        self._avg = None
        self._sum = 0
        self._count = 0

    def update(self, val: float, n: int = 1) -> None:
        self._val = val
        if val is not None:
            self._sum += val * n
            self._count += n
            self._avg = self._sum / self._count

    @property
    def avg(self) -> Optional[float]:
        return self._avg

    @property
    def val(self) -> float:
        return self._val

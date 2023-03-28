from __future__ import annotations

import json
import pathlib
import subprocess
from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from _typeshed import Self
else:
    Self = Any


def ffprobe(input_path: Union[str, pathlib.Path], **opts: Any) -> Any:
    _cmd = ["ffprobe"]
    _opts = ["-hide_banner", "-show_streams", "-of", "json", "-loglevel", "panic"]
    for k, v in opts.items():
        _opts.extend(["-" + str(k), str(v)])
    proc = subprocess.run(
        " ".join(_cmd + _opts + [str(input_path)]),
        shell=True,
        text=True,
        check=True,
        stdout=subprocess.PIPE,
    )
    return json.loads(proc.stdout)


class ffmpeg:
    _cmd: list[str]
    _output: Optional[str]
    _loglevel: str

    def __init__(self, y: bool = True, loglevel: str = "fatal") -> None:
        self._cmd = ["ffmpeg"]
        if y:
            self.y()
        self._output = None
        self._loglevel = loglevel

    def _opt(self, opt: str, *args: Any) -> ffmpeg:
        self._cmd.extend([opt] + [str(a) for a in args])
        return self

    def _compile(self) -> str:
        assert self._output is not None
        special_opts = [self._output, "-loglevel", self._loglevel]
        return " ".join(self._cmd + special_opts)

    def run(self, dry: bool = False, **kwargs: Any) -> str:
        command = self._compile()
        if not dry:
            subprocess.run(command, shell=True, **kwargs)
        return command

    def y(self) -> ffmpeg:
        return self._opt("-y")

    def i(self, arg: Any) -> ffmpeg:
        return self._opt("-i", arg)

    def f(self, arg: Any) -> ffmpeg:
        return self._opt("-f", arg)

    def r(self, arg: Any) -> ffmpeg:
        return self._opt("-r", arg)

    def ar(self, arg: Any) -> ffmpeg:
        return self._opt("-ar", arg)

    def ac(self, arg: Any) -> ffmpeg:
        return self._opt("-ac", arg)

    def vn(self) -> ffmpeg:
        return self._opt("-vn")

    def vf(self, arg: Any) -> ffmpeg:
        return self._opt("-vf", arg)

    def c_v(self, arg: Any) -> ffmpeg:
        return self._opt("-c:v", arg)

    def c_a(self, arg: Any) -> ffmpeg:
        return self._opt("-c:a", arg)

    def acodec(self, arg: Any) -> ffmpeg:
        return self.c_a(arg)

    def vcodec(self, arg: Any) -> ffmpeg:
        return self.c_v(arg)

    def ss(self, arg: float) -> ffmpeg:
        return self._opt("-ss", "%.3f" % arg)

    def to(self, arg: float) -> ffmpeg:
        return self._opt("-to", "%.3f" % arg)

    def qscale(self, arg: Any) -> ffmpeg:
        return self._opt("-qscale", arg)

    def qmin(self, arg: Any) -> ffmpeg:
        return self._opt("-qmin", arg)

    def qmax(self, arg: Any) -> ffmpeg:
        return self._opt("-qmax", arg)

    def qscale_v(self, arg: Any) -> ffmpeg:
        return self._opt("-qscale:v", arg)

    def qscale_a(self, arg: Any) -> ffmpeg:
        return self._opt("-qscale:a", arg)

    def threads(self, arg: Any) -> ffmpeg:
        return self._opt("-threads", arg)

    def audio_sync(self, arg: Any) -> ffmpeg:
        return self._opt("-async", arg)

    def map(self, arg: Any) -> ffmpeg:
        return self._opt("-map", arg)

    def output(self, arg: Union[str, pathlib.Path]) -> ffmpeg:
        self._output = str(arg)
        return self

    def loglevel(self, arg: str) -> ffmpeg:
        self._loglevel = str(arg)
        return self

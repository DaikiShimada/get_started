from __future__ import annotations

import datetime
import json
import os
import pathlib
import shutil
import sys
from typing import Any, Optional, Sequence, Union

import torch

from .aliases import _hostname_alias

__all__ = ["ArtifactManager"]


def _convert_dict_type(dic: dict[str, Any], *types: Any) -> dict[str, Any]:
    def _conv(val: Sequence) -> Union[str, Any]:
        for t in types:
            if isinstance(val, t):
                return str(val)
        return val

    return {
        k: _convert_dict_type(v, *types) if isinstance(v, dict) else _conv(v)
        for k, v in dic.items()
    }


class ArtifactManager(object):
    _run_dir: str
    _output: pathlib.Path

    @classmethod
    def get_cfg(cls) -> str:
        cfgs = [a for a in sys.argv if os.path.splitext(a)[-1] == ".cfg"]
        return cfgs[0][1:]

    @classmethod
    def gen_run_dir(cls, formatter: str) -> str:
        # date
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        run_dir = formatter.replace("%(date)", now)
        # hostname
        hostname = os.uname().nodename
        if hostname in _hostname_alias:
            hostname = _hostname_alias[hostname]
        run_dir = run_dir.replace("%(hostname)", hostname)
        # config name
        cfgname_key = "%(cfgname)"
        if cfgname_key in run_dir:
            cfg_name = os.path.splitext(os.path.basename(cls.get_cfg()))[0]
            run_dir = run_dir.replace(cfgname_key, cfg_name)
        return run_dir

    def __init__(
        self,
        output: Union[str, pathlib.Path],
        run_dir: str = "%(cfgname)_%(date)_%(hostname)",
    ) -> None:
        self._run_dir = self.gen_run_dir(run_dir)
        self._output = pathlib.Path(output) / self._run_dir
        self.output.mkdir(parents=True)

    def save_args(self, args: Any, name: str = "args.json") -> None:
        args_dict = _convert_dict_type(dict(args.__dict__), pathlib.Path)
        # pathlib to str
        with (self._output / name).open("w") as f:
            json.dump(args_dict, f, indent=2)

    def save_config(self) -> None:
        shutil.copy(self.get_cfg(), self._output)

    def save_command(self, name: str = "command.txt") -> None:
        with (self._output / name).open("w") as f:
            f.write("({})\n".format(pathlib.Path.cwd().absolute()))
            f.write(" ".join(sys.argv))

    def save_environ(self, name: str = "environ.txt") -> None:
        with (self._output / name).open("w") as f:
            f.write("\n".join(["{}={}".format(k, v) for k, v in os.environ.items()]))

    @property
    def output(self) -> pathlib.Path:
        return self._output

    @property
    def run_dir(self) -> str:
        return self._run_dir

    def save_checkpoint(
        self,
        model: torch.nn.Module,
        name: str = "model.pt.tar",
        optimizer: Optional[torch.optim.Optimizer] = None,
        **kwargs: Any,
    ) -> None:
        model_dev: torch.device = model.device  # type: ignore
        save_state = {
            "arch": type(model).__name__.lower(),
            "state_dict": model.to("cpu").state_dict(),
            "version": 2,
        }
        if optimizer:
            save_state["optimizer"] = optimizer.state_dict()

        for k, v in kwargs.items():
            save_state[k] = v
        torch.save(save_state, self._output / name)
        model.to(device=model_dev)

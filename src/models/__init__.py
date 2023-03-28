from __future__ import annotations

import argparse
import ast
from typing import Any

from .base import BaseModel


def _eval_dict_values(dic: dict[str, Any]) -> dict[str, str]:
    return {
        k: _eval_dict_values(v) if isinstance(v, dict) else ast.literal_eval(str(v))
        for k, v in dic.items()
    }


def _none_to_empty_dict(dic: dict[str, Any]) -> dict[str, Any]:
    return {k: {} if v is None else v for k, v in dic.items()}


def add_model_arguments(
    parser: argparse.ArgumentParser, config_action: str
) -> argparse.ArgumentParser:
    def _add_arguments(
        parser: argparse.ArgumentParser, name: str, action: str
    ) -> argparse.ArgumentParser:
        parser.add_argument(
            "--{}".format(name),
            type=str,
            default=None,
            help="name of {} model".format(name),
        )
        parser.add_argument(
            "--{}-config".format(name),
            type=str,
            nargs="*",
            action=action,
            help="config of {} model".format(name),
        )
        return parser

    for a in BaseModel.args():
        parser = _add_arguments(parser, a, config_action)
    return parser


def get_model_configs(obj: Any) -> dict:
    model_names = {a: getattr(obj, a, None) for a in BaseModel.args()}
    model_configs = _eval_dict_values(
        {c: getattr(obj, c, None) for c in BaseModel.config_args()}
    )
    model_configs = _none_to_empty_dict(model_configs)
    return {**model_names, **model_configs}


def build_models(time_dim: int, n_class: int, **kwargs: Any) -> BaseModel:
    return BaseModel(time_dim, n_class, **kwargs)

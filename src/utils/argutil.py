from __future__ import annotations

import argparse
from typing import Any, Callable, Optional, Sequence, Union


class ConfigArgumentParser(argparse.ArgumentParser):
    def convert_arg_line_to_args(self, arg_line: str) -> list[str]:
        return arg_line.split() if not arg_line.startswith("#") else ""  # type: ignore


class AnyOptParser(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence, None],
        option_string: Optional[str] = None,
    ) -> None:
        opt_dict = getattr(namespace, self.dest, [])
        if opt_dict is None:
            opt_dict = {}
        if not isinstance(values, list):
            values = [values]
        for v in values:
            key, opt = v.split("=")
            opt_dict[key] = opt
        setattr(namespace, self.dest, opt_dict)


def _to_argstring(key: str, value: Union[bool, Sequence]) -> str:
    def is_iterable(container: Sequence) -> bool:
        try:
            for _ in container:
                pass
        except Exception:
            return False
        else:
            return True

    arg_str = ""
    key = key.replace("_", "-")
    if isinstance(value, bool):
        if value:
            arg_str = "--{}".format(key)
    else:
        value_str = (
            " ".join([str(v) for v in value])
            if not isinstance(value, str) and is_iterable(value)
            else str(value)
        )
        arg_str = "--{}={}".format(key, value_str)
    return arg_str


def _parse_arg(
    parser: argparse.ArgumentParser, *args: Any, **kwargs: Any
) -> argparse.Namespace:
    a = list(args) + [_to_argstring(k, v) for k, v in kwargs.items()]
    a = list(filter(lambda x: len(x) > 0, a))
    _args = parser.parse_args(args=a)
    return _args


def _parse_known_arg(
    parser: argparse.ArgumentParser, *args: Any, **kwargs: Any
) -> tuple[Any, ...]:
    a = list(args) + [_to_argstring(k, v) for k, v in kwargs.items()]
    a = list(filter(lambda x: len(x) > 0, a))
    args = parser.parse_known_args(args=a)
    return args


def getarg(parser: argparse.ArgumentParser, *args: Any, **kwargs: Any) -> Callable:
    def wrapper(f: Callable) -> Callable:
        def _f(*fargs: Any, **fkwargs: Any) -> Any:
            # check function args (given or not given)
            if len(fargs) > 0 or len(fkwargs) > 0:
                # parse from function args
                a = _parse_arg(parser, *fargs, **fkwargs)
            else:
                # parse from default source
                a = _parse_arg(parser, *args, **kwargs)
            return f(a)

        return _f

    return wrapper


def getknownarg(parser: argparse.ArgumentParser, *args: Any, **kwargs: Any) -> Callable:
    def wrapper(f: Callable) -> Callable:
        def _f(*fargs: Any, **fkwargs: Any) -> Any:
            # check function args (given or not given)
            if len(fargs) > 0 or len(fkwargs) > 0:
                # parse from function args
                a, _ = _parse_known_arg(parser, *fargs, **fkwargs)
            else:
                # parse from default source
                a, _ = _parse_known_arg(parser, *args, **kwargs)
            return f(a)

        return _f

    return wrapper


def _add_arguments(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument(
        "--{}".format(name),
        type=str,
        default=None,
        help="name of {} model".format(name),
    )
    parser.add_argument(
        "--{}-config".format(name),
        type=str,
        default=None,
        action=AnyOptParser,
        help="config of {} model".format(name),
    )

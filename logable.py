# Python logable wrapper.

# (c) JoBe, 2025


import functools
import types

from collections.abc import Callable
from typing import TypeVar, ParamSpec


P = ParamSpec("P")
R = TypeVar("R")


__all__ = [
    "Logable",
]


class Logable:
    def __init__(self, logger: object, level: str = "info") -> None:
        self.logger = logger
        self.level = level.lower()

    def __call__(self, obj: Callable[P, R]) -> Callable[P, R]:
        if not isinstance(obj, (type, types.FunctionType)):
            raise TypeError(f"invalid object supplied to @{self.logger}.logable")

        @functools.wraps(obj)
        def inner(*args: P.args, **kwargs: P.kwargs):
            res = obj(*args, **kwargs)
            #if isinstance(res, LogResult):
            #    res = res.__log__()

            self.logger.log(f"{obj.__qualname__}("
                            f"{', '.join(str(a) for a in args)}, "
                            f"{', '.join(f'{k}={v}' for k, v in kwargs.items())} "
                            f"returned {res!r}")

        return inner

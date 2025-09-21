# Python logable wrapper.

# (c) JoBe, 2025


import functools
import types


__all__ = [
    "Logable"
]


class Logable:
    def __init__(self, logger: object, level: str = "info") -> None:
        self.logger = logger
        self.level = level.lower()

    def __call__(self, obj: type | types.FunctionType) -> ...:
        if not isinstance(obj, (type, types.FunctionType)):
            raise TypeError(f"invalid object supplied to @{self.logger}.logable")

        @functools.wraps()
        def inner(*args, **kwargs):
            res = obj(*args, **kwargs)
            if isinstance(res, LogResult):
                res = res.__log__()

            self.logger.log(f"{obj.__qualname__}("
                            f"{', '.join(str(a) for a in args}, "
                            f"{', '.join(f'{k}={v}' for k, v in kwargs.items())} "
                            f"returned {res!r}")

        return inner

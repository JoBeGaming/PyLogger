# Logger
# TODO: log.BASE_PATH, rights

# pyright: reportSelfClsParameterName=false

import sys

from collections.abc import Generator
from datetime import datetime
from time import time
from pathlib import Path
from time import time
from typing import Literal, Never, TextIO, override, Any


class logError(Exception):
    """Base Class for all logging related Errors."""


def get_path() -> str:
    # Generate a random string, consisting
    # of the current time as a Hex String
    ct = str(hex(int(str(time()).replace(".", ""))))
    try:
        with open(f"log_{ct}.log", "r", errors="strict") as file: 
            file.close()
            return get_path()
    except FileNotFoundError:
        return f"log_{ct}.log"


class BaseLogger():

    # These are defined as a kind of stub, so Mypy doesn't complain
    def compile(log: BaseLogger, **kwargs: Any) -> str: 
        return ""

    def decompile(log: BaseLogger, line: str) -> tuple[str, str, str]: 
        return ("", "", "")

    def __init__(log: BaseLogger, new_path: str = "") -> None: 
        """Initiate a new log at `logs/`, except another path is given"""
        log.__init(new_path)

    def __init(log: BaseLogger, new_path: str = "") -> None:
        if not new_path:
            new_path = rf"logs/{get_path()}"
        log.PATH = f"{new_path.removesuffix('.log')}.log"

        try:  
            with open(log.PATH, "x", errors="strict"):
                pass
            log.newEntry(msg=f"Initiated file as {log.PATH}", level="Info")
        except FileNotFoundError:
            backslash = "\\"
            log.__init(rf"{str(__file__).replace(backslash, "/").removesuffix("logger.py")}logs/{get_path().removesuffix(".log")}")

    def newEntry(log: BaseLogger, msg: str, level: str) -> None:
        """Log to existing log, or create a new one and log to that one if needed."""
        try:
            with open(log.PATH, "a", errors="strict") as file:
                file.write(log.compile(msg=msg, level=level))
        except NameError:
            log.__init()
            log.newEntry(msg, level)

    def get_contents(log: BaseLogger) -> tuple[tuple[str, str, str], ...]:
        contents: tuple[tuple[str, str, str], ...] = ()
        with open(log.PATH, "r") as file:
            for line in file.readlines():
                contents += (log.decompile(line),)

        return contents

    #TODO make str of op be literals
    def _compare(log: BaseLogger, time: str, filter_time: str, op: str) -> bool:
        if len(op) == 2:
            return log._compare(time, filter_time, op[0]) or time == filter_time

        if op[0] == "=":
            return time == filter_time
        elif op[0] == "!":
            return time != filter_time
        elif op[0] == "<":
            time = time.replace(".", "")
            filter_time = filter_time.replace(".", "")
            index = 0

            for char in time:
                if int(char) < int(filter_time[index]):
                    return True
                elif int(char) > int(filter_time[index]):
                    return False

            return False
        else:
            return not log._compare(time, filter_time, "<") and not time == filter_time

    def get_time(log: BaseLogger, filter_time: str, op: str = ">=") -> tuple[tuple[str, str, str], ...]:
        if op not in {
            ">",
            ">=",
            "==",
            "<=",
            "<",
            "!="
        }:
            raise TypeError(f"invalid operation {op}, expected comparison")
        contents: tuple[tuple[str, str, str], ...] = ()
        for time, level, msg in log.get_contents():
            if log._compare(time, filter_time, op):
                contents += ((time, level, msg),)

        return contents

    def dump(log: BaseLogger, file: TextIO = sys.stdout, ignore: tuple[str, ...] = ()) -> None:
        print(f"Log {log} at {log.PATH}")
        for time, level, msg in log.get_contents():
            if not level in ignore:
                print(log.compile(time=time, level=level, msg=msg).removesuffix("\n\n"), file=file)

    # TODO
    def clear(log: BaseLogger, *, keep: tuple[str, ...] = (), time: str = "", op: str = "") -> None:
        if not keep and not time and not op:
            with open(log.PATH, "w"): 
                pass
        else:
            ...

    def delAll(log: BaseLogger) -> None:
        """Delete all logs, except the latest."""
        #TODO: Filter thru the parents if needed (count slashes when defining path)
        #TODO this deletes current log too lol
        directory = Path(log.PATH).parent
        for file in directory.iterdir():
            if file.is_file() and file.suffix == ".log" and file.name != log.PATH:
                file.unlink()

    def newPath(log: BaseLogger, path: str) -> None:
        log.__init(path)

    def extensiveError(log, obj: BaseException | Exception) -> None: #TODO
        tb = obj.__traceback__
        log.newEntry(f"{obj}, traceback to {getattr(tb, "tb_frame", "-")}", level="Error")
        log.newEntry(f"Traceback object at {tb}", level="Error")
        log.newEntry(f"TB Lasti: {getattr(tb, "tb_lasti", "-")}", level="Error")
        log.newEntry(f"TB Lineno: {getattr(tb, "tb_lineno", "-")}", level="Error")
        log.newEntry(f"TB Next: {getattr(tb, "tb_next", "-")}", level="Error")
        log.newEntry(f"Exiting Program", level="Fatal")

    def debug(log, msg: str) -> None:
        log.newEntry(msg, level="Debug")

    def info(log, msg: str) -> None:
        log.newEntry(msg, level="Info")

    def error(log, msg: str) -> None:
        log.newEntry(msg, level="Error")

    def fatal(log, error: Exception, msg: str) -> Never:
        log.newEntry(f"{error}: {msg}", level="Fatal")
        raise error

    def current_path(log) -> str:
        return log.PATH

    def __init_subclass__(cls, **kwargs: dict[str, Any]):
        for attr in {"compile", "decompile"}:
            if not attr in cls.__dict__:
                raise TypeError(f"BaseLogger subclass must define {attr}")

class logger(BaseLogger):
    levels = Literal["Debug", "Info", "Error", "Fatal"]

    @override
    def compile(log: logger, /, *, msg: str = "", time: str = "", level: logger.levels = "Debug") -> str:
        if not time:
            now = datetime.now()
            time = f"{now.strftime('%H:%M:%S.')}" + f"{now.microsecond // 1000:03d}"
        return f"{time} [{level}]: {msg}\n"

    @override
    def decompile(log: logger, line: str) -> tuple[str, str, str]:
        time = line.split()[0]
        level = line.removeprefix(f"{time} [").split("]")[0]
        msg = line.removeprefix(f"{time} [{level}]: ")
        return (time, level, msg)


class SecureLogError(BaseException):
    """"""


class SafeLogger:

    def __init__(log: SafeLogger, new_path: str, request: tuple[tuple[str, int], ...] = ()) -> None:
        log.requests = request
        log.PATH = new_path
        import secrets
        log.ADMIN_SEED = secrets.token_hex(5)
        log.BASE_SEED = secrets.token_hex(5)
        log.SEC_SEED = secrets.token_hex(5)
        directory = Path(log.PATH)
        try:
            for file in directory.iterdir():
                if file.is_file() and file.name == log.PATH:
                    raise SecureLogError(f"File {log.PATH} already exists")
        except FileNotFoundError:
            pass
        with open(log.PATH, "x"):
            pass


    def getseed(log: SafeLogger, access_type: str) -> str:
        if access_type.lower() == "admin":
            return log.ADMIN_SEED
        base = log.BASE_SEED
        n: int = 0
        for char in access_type.lower():
            n += ord(char) - ord('z') + 1
        return hex(n >> int(base, base=16) & int(log.SEC_SEED, base=16))

    def get_total(log: SafeLogger):
        total = -1
        while True:
            total += 1
            yield total
            yield total

    def stamp(log: SafeLogger, key: str, generator: Generator[int], *, additional: int = 0) -> Generator[tuple[str, int]]:
        total_additional = 0
        while True:
            if not additional:
                import secrets
                additional = int(secrets.token_hex(16), base=16)
            total_additional += additional
            total = next(generator)
            # * Security flaw: 
            #   The first `total_additional` is exposed to the following calls, 
            #   so long as there is no stamp with a `additional` given, the first
            #   `additional` is exposed.  Sadly that one happens to be reserved for
            #   admin keys.  We could try and prevent issues, by stamping fake keys
            #   and updating `total`.
            yield f"{hex(id(log))}-{key}-{hex(id(key))}--{hex(total_additional)}-{hex(total)}", total

    def request_keys(log: SafeLogger):
        k = getattr(log, "k", None)
        if k:
            delattr(log, "k")
        # `k` is the admin key, and if provided
        # we return all keys, else we return None
        # after it has been called a first time
        keys: tuple[tuple[str, ...], ...] = ()
        import secrets
        global_total = log.get_total()
        admin_key: str = secrets.token_hex(64) + f"-{log.getseed("admin")}"
        admin_key = next(log.stamp(admin_key, global_total, additional=int(secrets.token_hex(16), base=16)))[0]
        assert int(admin_key.split("-")[-1], base=16) == 0
        next(global_total)
        total = 1
        gt = 0
        for access_type, repeat in log.requests:
            subkeys: tuple[str, ...] = ()
            for _ in range(repeat):
                import secrets
                key_: str = secrets.token_hex(64) + log.getseed(access_type)
                key = next(log.stamp(key_, global_total))
                lt = key[1]
                gt = next(global_total)
                assert int(key[0].split("-")[-1], base=16) == gt == lt == total
                total += 1
                subkeys += (key[0],)
            keys += (subkeys,)
        yield admin_key, keys
        while True:
            if not k is admin_key:
                yield None
            else:
                yield keys

n = SafeLogger(get_path())
key_g = n.request_keys()
admin_key = next(key_g)
print(admin_key)
print(next(key_g))
print(next(key_g))
print(next(key_g))
n.k = admin_key
print(next(key_g))

log = logger()
for i in range(1000):
    log.newEntry("hi", "Info")
log.dump()
log.clear()
log.delAll()
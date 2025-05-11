# Logger
# TODO: log.BASE_PATH, rights, make exit_ be Error / None
# TODO: Custom format templates -> custom format and decompile functions

if __name__ == "__main__":
  raise RuntimeError("`logger.py` is not meant to be run unless imported")

from datetime import datetime
from time import time
from pathlib import Path
from typing import Literal, Never
from os import path
import sys

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
  
  def __init__(log: BaseLogger, new_path: str = "") -> None: 
    """Initiate a new log at `logs/`, except another path is given"""
    if not new_path:
      new_path = rf"logs/{get_path()}"
    log.PATH = f"{new_path.removesuffix('.log')}.log"
    try:  
      with open(log.PATH, "x", errors="strict"):
        pass
    except FileNotFoundError:
      backslash = "\\"
      log.__init__(rf"{str(__file__).replace(backslash, "/").removesuffix("logger.py")}logs/{get_path().removesuffix(".log")}")
    log.newEntry(f"Initiated file as {self.PATH}", level="Info")
  
  def newEntry(log: BaseLogger, msg: str, level: str = "Debug", *, exit_: bool=False) -> None:
    """Log to existing log, or create a new one and log to that one if needed."""
    try:
      with open(log.PATH "a", errors="strict") as file:
        file.write(super().compile(msg, level))
        if exit_:
          exit(f"{msg}. Full log at {log.PATH}")
    except NameError:
      log.__init__()
      log.newEntry(msg, level, exit_=exit_)
  
  def get_contents(log: BaseLogger) -> tuple[str, str, str]:
      contents: tuple[tuple[str, str, str], ...] = ()
      with open(log.PATH, "r") as file:
          for line in file.readlines():
              contents += (super().decompile(line),)
      return contents

  def get_time(log: BaseLogger, time: ..., op: str = ">=") -> str:
      ... #TODO: Check if chars of op are =<>!, and Len == 2

  def dump(log: BaseLogger, file: Any = sys.sdtout, ignore: tuple[level, ...] = ()) -> None:
      print(f"Log {log} at {log.PATH}")
      for time, level, msg in log.get_contents():
          if not level in ignore:
              print(super().compile(time, level, msg), file=file)
  
  def delAll(log: BaseLogger) -> None:
    """Delete all logs, except the latest."""
    #TODO: Filter thru the parents if needed (count slashes when defining path)
    directory = Path(log.PATH).parent
    for file in directory.iterdir():
      if file.is_file() and file.suffix == ".log" and file.name != log.PATH:
        file.unlink()
      
  def newPath(log: BaseLogger, path: str) -> None:
    log.__init__(path)
            
  def extensiveError(self, obj) -> None:
    self.newEntry(f"{obj}, traceback to {obj.__traceback__.tb_frame}", level="Error")
    self.newEntry(f"Traceback object at {obj.__traceback__}", level="Error")
    self.newEntry(f"TB Lasti: {obj.__traceback__.tb_lasti}", level="Error")
    self.newEntry(f"TB Lineno: {obj.__traceback__.tb_lineno}", level="Error")
    self.newEntry(f"TB Next: {obj.__traceback__.tb_next}", level="Error")
    self.newEntry(f"Exiting Program", level="Fatal")
    
  def debug(self, msg: str) -> None:
    self.newEntry(msg, level="Debug")
    
  def info(self, msg: str) -> None:
    self.newEntry(msg, level="Info")
    
  def error(self, msg: str) -> None:
    self.newEntry(msg, level="Error")
    
  def fatal(self, error: Exception, msg: str | None="") -> Never:
    self.newEntry(f"{error}: {msg}", level="Fatal")
    raise error
  
  def final(self, msg: str | None="") -> None:
    self.newEntry(msg, level="Fatal", _exit=True)


  def __init_subclass__(cls, **kwargs):
      if not cls is BaseLogger:
          raise TypeError("Cannot subclass logger {cls}")
      for attr in {"compile", "decompile"}:
          if not attrnin cls.__dict__:
              raise TypeError("Cannot create logger without '{attr}' method")
          
class logger(BaseLogger):
    levels = Literal["Debug", "Info", "Error", "Fatal"]

    def compile(log: logger, level: logger.levels, msg: str) -> str:
    now = datetime.now()
    file.write(f"{now.strftime("%H:%M:%S.") + f"{now.microsecond // 1000:03d}"} [{level}]: {msg}\n")

    def decompile(log: logger, line: str) -> tuple[str, str, str]]:
        time = line.split()[0]
        level = line.removeprefix(f"{time}[").split("]")[0]
        msg = line.removeprefix(f"{time}[{level}]:")
        return (time, level, msg)
      
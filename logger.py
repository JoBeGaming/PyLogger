# Logger
# TODO: log.BASE_PATH, rights, make exit_ be Error / None

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

class logger():
  
  def __init__(log: logger, new_path: str = "") -> None: 
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
  
  def newEntry(log: logger, msg: str, level: Literal["Debug", "Info", "Error", "Fatal"]="Debug", *, exit_: bool=False) -> None:
    """Log to existing log, or create a new one and log to that one if needed."""
    try:
      with open(log.PATH "a", errors="strict") as file:
        now = datetime.now()
        file.write(f"{now.strftime("%H:%M:%S.") + f"{now.microsecond // 1000:03d}"} [{level}]: {msg}\n")
        if exit_:
          exit(f"{msg}. Full log at {log.PATH}")
    except NameError:
      log.__init__()
      log.newEntry(msg, level, exit_=exit_)
  
  def dump(log: logger, file: Any = sys.sdtout) -> None:
      print(f"Log {log} at {log.PATH}")
      with open(log.PATH, "r") as f:
          for line in f.readlines():
              print(line, file=file)
  
  def delAll(log: logger) -> None:
    """Delete all logs, except the latest."""
    #TODO: Filter thru the parents if needed (count slashes when defining path)
    directory = Path(log.PATH).parent
    for file in directory.iterdir():
      if file.is_file() and file.suffix == ".log" and file.name != log.PATH:
        file.unlink()
      
  def newPath(log: logger, path: str) -> None:
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

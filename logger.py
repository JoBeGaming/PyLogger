# Logger

if __name__ == "__main__":
  raise RuntimeError("`logger.py` is not meant to be run unless imported")

from datetime import datetime
from time import time
from pathlib import Path
from typing import Literal, Never
from os import path

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
  
  def __init__(self, newPath: str | None=None) -> None: 
    """Initiate a new log at `logs/`, except another path is given"""
    if newPath is None:
      newPath = rf"logs/{get_path()}"
    self.LOG_PATH = f"{newPath}.log"
    try:  
      with open(self.LOG_PATH, "x", errors="strict"):
        pass
    except FileNotFoundError:
      backslash = "\\"
      self.__init__(rf"{str(__file__).replace(backslash, "/").removesuffix("logger.py")}logs/{get_path().removesuffix(".log")}")
    self.newEntry(f"Initiated file as {self.LOG_PATH}", level="Info")
  
  def newEntry(self, msg: str, level: Literal["Debug", "Info", "Error", "Fatal"]="Debug", *, _exit: bool=False) -> None:
    """Log to existing log, or create a new one and log to that one if needed."""
    try:
      with open(self.LOG_PATH, "a", errors="strict") as file:
        now = datetime.now()
        file.write(f"{now.strftime("%H:%M:%S.") + f"{now.microsecond // 1000:03d}"} [{level}]: {msg}\n")
        if _exit:
          exit(f"{msg}. Full log at {self.currentPath()}")
    except NameError:
      self.__init__()
      self.newEntry(msg, level)
  
  def currentPath(self) -> str:
    """Return the current Path of the log."""
    try:
      return self.LOG_PATH
    except NameError: 
      raise logError
  
  def delAll(self) -> None:
    """Delete all logs, except the latest."""
    directory = Path(self.LOG_PATH).parent
    for file in directory.iterdir():
      if file.is_file() and file.suffix == ".log" and file.name != self.LOG_PATH:
        file.unlink()
      
  def newPath(self, newPath: str) -> None:
    self.__init__(newPath)
            
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

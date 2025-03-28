# Logger
A Python Logger, made as simple as possible, whilst only using Python.
Each new Logger Instance can get new unique Attributes, allowing for Logs that do stuff for Internal and External needs.

## Functions:
- get_path: Return a newly generated path, using the `dir` specified beforehand.

## Classes:
- logError: Generic Error that happens whilst Logging.
- logger:
  - __init__: Initialize the Log, if given, use the Path, else generate a new one using `get_path`.
  - newEntry: Initialize the Log if that has not been done yet, then append the `message` with the given `level`.
  - currentPath: Return the Path the instance of the Logger is currently using.
  - delAll: Delete All Logs in the Log Directory, except the current Log.
  - newPath: Initialize the Log and use the given Path.
  - extensiveError: Log any given Error extensively.
  - debug: Append the `message` to the current log, using the Debug Level.
  - info: Append the `message` to the current log, using the Info Level.
  - error: Append the `message` to the current log, using the Error Level.
  - Fatal: Append the `message` to the current log, using the Fatal Level, then exit.

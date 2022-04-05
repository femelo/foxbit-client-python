import os
from logging import Logger, FileHandler, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from datetime import datetime
from colorama import Fore, Style

COLORMAP = {
    NOTSET: Fore.RESET,
    DEBUG: Fore.CYAN,
    INFO: Fore.GREEN,
    WARNING: Fore.YELLOW,
    ERROR: Fore.LIGHTRED_EX,
    CRITICAL: Fore.RED
}

COLOR_RESET = Style.RESET_ALL

class RotatingFileLogger(Logger):
    def __init__(self, name, folder, encoding='utf-8', level=DEBUG, maxFileSize=20):
        self.folder = folder
        self.seqNumber = 0
        self.dateTime = None
        self.maxFileSize = maxFileSize * 1024 * 1024
        self.encoding = encoding
        if not os.path.exists(folder):
            os.mkdir(folder)
        super().__init__(name, level=level)

    def rotateFile(self):
        startNewHandler = False
        dateTime = datetime.now().strftime("%Y-%m-%d")
        if not self.hasHandlers():
            self.seqNumber = 1
            self.dateTime = dateTime
            startNewHandler = True
        else:
            if dateTime != self.dateTime:
                self.seqNumber = 1
                self.dateTime = dateTime
                startNewHandler = True
            elif os.path.getsize(self.handlers[-1].baseFilename) > self.maxFileSize:
                self.seqNumber += 1
                startNewHandler = True
            else:
                pass
        
        if startNewHandler:
            if self.hasHandlers():
                self.handlers[-1].close()
            self.handlers.clear()
            filePath = os.path.join(
                self.folder, 
                '-'.join([self.name, self.dateTime, str(self.seqNumber)]) + '.log'
            )
            self.addHandler(FileHandler(filePath, encoding=self.encoding))

    def callHandlers(self, record):
        self.rotateFile()
        super().callHandlers(record)

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        color_msg = COLORMAP[level] + msg + COLOR_RESET
        super()._log(level, color_msg, args, exc_info, extra, stack_info)

class DefaultLogger(RotatingFileLogger):
    def __init__(self, encoding='utf-8', level=DEBUG, maxFileSize=20):
        super().__init__(
            folder="logs", 
            name="foxbit-client", 
            encoding=encoding, 
            level=level, 
            maxFileSize=maxFileSize)

class WebSocketLogger(RotatingFileLogger):
    def __init__(self, encoding='utf-8', level=DEBUG, maxFileSize=20):
        super().__init__(
            folder="logs", 
            name="foxbit-client-websocket", 
            encoding=encoding, 
            level=level, 
            maxFileSize=maxFileSize)

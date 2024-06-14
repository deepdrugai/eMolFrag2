import logging

global log

try:  # if colorlog is installed, get colored log files
    import colorlog

    class CustomFormatter(colorlog.ColoredFormatter):
        def format(self, record):
            # Modify record.pathname here before calling the parent class's format method
            # This example gets the part of the path after "eMolFrag"
            record.pathname = record.pathname.split("eMolFrag/")[-1]
            return super().format(record)

    # Then, when setting up your logger, use the custom formatter:
    formatter = CustomFormatter(
        fmt="%(log_color)s%(asctime)s [%(levelname)s: %(pathname)s:%(lineno)d::%(funcName)s] - %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = colorlog.StreamHandler()
    handler.setFormatter(formatter)

    log = colorlog.getLogger(__name__)
    log.addHandler(handler)
except ImportError:  # pragma: no cover'

    class CustomLogger(logging.getLoggerClass()):
        def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
            record = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
            record.pathname = record.pathname.split("eMolFrag/")[-1]
            return record

    logging.setLoggerClass(CustomLogger)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s: %(pathname)s:%(lineno)d::%(funcName)s] - %(message)s",
        # format="%(log_color)s%(asctime)s [%(levelname)s: %(filename)s::%(funcName)s:%(lineno)d] - %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log = logging.getLogger(__name__)
    log.warning("Colorlog not installed.")

log.setLevel("DEBUG")

# log.debug('This is my 😂 debug message ')
# log.info('This is my 💜 info message ')
# log.warning('This is my 🤔 warning message ')
# log.error('This is my error 😱message ')
# log.critical('This is my 😭 critical message ')

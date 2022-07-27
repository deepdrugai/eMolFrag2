import logging
global log

try: # if colorlog is installed, get colored log files
    import colorlog
    colorlog.basicConfig(
        format="%(log_color)s%(asctime)s [%(levelname)s: %(pathname)s:%(lineno)d::%(funcName)s] - %(message)s%(reset)s",
        # format="%(log_color)s%(asctime)s [%(levelname)s: %(filename)s::%(funcName)s:%(lineno)d] - %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        # ,
        # filename = "logfile.log",
        # filemode = "w"
    )
    log = colorlog.getLogger(__name__)
except ImportError as e:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s: %(pathname)s:%(lineno)d::%(funcName)s] - %(message)s",
        # format="%(log_color)s%(asctime)s [%(levelname)s: %(filename)s::%(funcName)s:%(lineno)d] - %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    log = logging.getLogger(__name__)
    log.debug('Colorlog not installed.')

log.setLevel("DEBUG")

# log.debug('This is my 😂 debug message ')
# log.info('This is my 💜 info message ')
# log.warning('This is my 🤔 warning message ')
# log.error('This is my error 😱message ')
# log.critical('This is my 😭 critical message ')
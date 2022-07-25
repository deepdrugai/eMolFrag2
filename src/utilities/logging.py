import colorlog, logging
import sys

colorlog.basicConfig(
    format="%(log_color)s%(asctime)s [%(levelname)s: %(pathname)s:%(lineno)d::%(funcName)s] - %(message)s%(reset)s",
    # format="%(log_color)s%(asctime)s [%(levelname)s: %(filename)s::%(funcName)s:%(lineno)d] - %(message)s%(reset)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    # ,
    # filename = "logfile.log",
    # filemode = "w"
)

global logger

logger = colorlog.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# logger.debug('This is my 😂 debug message ')
# logger.info('This is my 💜 info message ')
# logger.warning('This is my 🤔 warning message ')
# logger.error('This is my error 😱message ')
# logger.critical('This is my 😭 critical message ')
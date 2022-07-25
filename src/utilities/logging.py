import logging
global logger

try:
    import colorlog
    colorlog.basicConfig(
        format="%(log_color)s%(asctime)s [%(levelname)s: %(pathname)s:%(lineno)d::%(funcName)s] - %(message)s%(reset)s",
        # format="%(log_color)s%(asctime)s [%(levelname)s: %(filename)s::%(funcName)s:%(lineno)d] - %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        # ,
        # filename = "logfile.log",
        # filemode = "w"
    )
    logger = colorlog.getLogger(__name__)
except ImportError as e:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s: %(pathname)s:%(lineno)d::%(funcName)s] - %(message)s",
        # format="%(log_color)s%(asctime)s [%(levelname)s: %(filename)s::%(funcName)s:%(lineno)d] - %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger('my_logger')

logger.setLevel(logging.DEBUG)

# logger.debug('This is my 😂 debug message ')
# logger.info('This is my 💜 info message ')
# logger.warning('This is my 🤔 warning message ')
# logger.error('This is my error 😱message ')
# logger.critical('This is my 😭 critical message ')
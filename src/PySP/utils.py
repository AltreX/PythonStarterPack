import functools
import logging
import argparse
from rich.logging import RichHandler
from rich.console import Console

NM_LOG_FORMAT = (
    "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) : %(message)s")


def remove_handlers() -> None:
    logger = logging.getLogger()
    for handler in logger.handlers:
        if type(handler) == type(RichHandler()):
            logger.removeHandler(handler)
    if not logger.hasHandlers():
        logger.addHandler(logging.NullHandler())


def setup_console_logger(
        level:int=logging.INFO,
        markup:bool=True,
        console:Console=None) -> None:

    console_handler = RichHandler(
        rich_tracebacks=True,
        omit_repeated_times=False,
        console=console,
        markup=markup)

    logger = logging.getLogger()
    logger.setLevel(level)
    # check if there is already a console handler and remove it if yes
    for handler in logger.handlers:
        if type(handler) == type(console_handler):
            logger.removeHandler(handler)
    # add the new handler with the required configuration
    logger.addHandler(console_handler)


def setup_file_logger(
        filename:str,
        level:int=logging.DEBUG) -> None:
    file = logging.FileHandler(filename)
    file.setFormatter(logging.Formatter(NM_LOG_FORMAT))
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(file)


def add_options(*options):
    def decorator_add_options(func):
        @functools.wraps(func)
        def wrapper_add_options(*args, **kwargs):
            p:argparse.ArgumentParser = func(*args, **kwargs)
            if "verbose" in options:
                p.add_argument("-v", "--verbose",
                               action="store_true",
                               help="enable debug logging if provided")
            if "silent" in options:
                p.add_argument("-s", "--silent",
                               action="store_true",
                               help="disable console logging")
            if "log_file" in options:
                p.add_argument("-l", "--log_file",
                               action="store_const",
                               const=f"{__name__.split('.')[0]}.log",
                               help="enable file logging to the path provided"
                               + "or defaults to the top module name or "
                               + "package name")
            if "logrotate" in options:
                p.add_argument("--sized_logrotate",
                            action="store_true",
                            help="use sized log rotate, default values rotate"
                            " at 5MBytes and keep until 20 files (100MBytes)",)
                p.add_argument("--timed_logrotate",
                            action="store_true",
                            help="use timed log rotate, default values rotate"
                            " at midnight and keep until 20 files (20 days)",)
                p.add_argument("--maxbytes",
                            action="store",
                            help="maxBytes value for sized log rotate, default"
                            " is 5 000 000 (5MBytes)",
                            type=int,
                            default=5000000,
                            metavar="BYTES",)
                p.add_argument("--backupcount",
                            action="store",
                            help="backupCount value for all types of log "
                            "rotate, default is 20 files",
                            type=int,
                            default=20,
                            metavar="COUNT",)
                p.add_argument("--when",
                            action="store",
                            help="when value for timed log rotate, default is "
                            "rotate at midnight, see https://docs.python.org/"
                            "3/library/logging.handlers.html#"
                            "timedrotatingfilehandler for more details of the "
                            "when option",
                            type=str,
                            default="midnight",
                            metavar="WHEN",)
            return p
        return wrapper_add_options
    return decorator_add_options


def print_except():
    from rich.console import Console
    c = Console()
    c.print_exception(show_locals=True)
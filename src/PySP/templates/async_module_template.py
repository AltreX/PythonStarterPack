import asyncio
import argparse # https://docs.python.org/3/library/argparse.html
import logging # https://docs.python.org/3/library/logging.html

from pathlib import Path # https://docs.python.org/3/library/pathlib.html
from collections.abc import Callable

from . import utils


log = logging.getLogger(__name__)


async def main() -> None:
    """Main function, where everything starts and ends"""

    # argument parser initialization
    args = arg_parser().parse_args()

    # Set the log level based on the verbose argument status
    level = logging.DEBUG if args.verbose else logging.INFO

    # Disabling standard output logging if silent has been set True
    if not args.silent:
        utils.setup_console_logger(level)
    else:
        utils.remove_handlers()

    # Set up the log file based on the log file argument status
    if args.log_file:
        utils.setup_file_logger(args.log_file, level)

    log.info(f"main start")

    ###
    #
    # Your code here
    #
    ###

    log.info(f"main end")


async def polling_loop(functions:list[Callable], timer):
    """Polling loop utility that can be used to setup reccurent call
    to function in specific intervals
    
    :param functions: list of function to call
    :type functions: list[Callable]
    :param timer: timer in second to wait for next call
    :type timer: float
    """
    try:
        logging.info("starting polling loop")
        while True:
            for f in functions:
                f()
            await asyncio.sleep(timer)
    except asyncio.CancelledError:
        logging.info("polling loop stopped")


@utils.add_options("verbose", "log_file", "silent", "logrotate")
def arg_parser() ->  argparse.ArgumentParser:
    # parser configuration for this module
    p = argparse.ArgumentParser(
        prog="",
        description=""
    )

    return p

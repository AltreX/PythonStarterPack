import argparse # https://docs.python.org/3/library/argparse.html
import logging # https://docs.python.org/3/library/logging.html

from pathlib import Path # https://docs.python.org/3/library/pathlib.html

from . import utils


log = logging.getLogger(__name__)


def main() -> None:
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

    log.info(f"starting")

    ###
    #
    # Your code here
    #
    ###

    log.info(f"stopping")


@utils.add_options("verbose", "log_file", "silent", "logrotate")
def arg_parser() ->  argparse.ArgumentParser:
    # parser configuration for this module
    p = argparse.ArgumentParser(
        prog="",
        description=""
    )

    return p

import sys
import logging
from .PySP import main
from .utils import setup_console_logger


if __name__ == '__main__':
    setup_console_logger()
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        from rich.console import Console
        c = Console()
        c.print_exception(show_locals=True)
    sys.exit(rc)
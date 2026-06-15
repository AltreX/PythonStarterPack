import sys
import logging
{% if asynchronus %}
import asyncio
import signal
{% endif %}
from .{{ project_name }} import main
from .utils import setup_console_logger


setup_console_logger()
log = logging.getLogger(__name__)

{% if asynchronus %}
async def shutdown(signal: signal.Signals, loop:asyncio.BaseEventLoop):
    """Cleanup tasks tied to the service's shutdown.
    
    :param signal: the received signal
    """
    # print used to return after the "^C" console artifact, making the
    # next log start cleanly
    print()
    log.info(f"Received exit signal {signal.name}...")

    tasks = set()

    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            tasks.add(task)
            task.cancel()

    log.info(f"Cancelling {len(tasks)} remaining tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    for s in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

    try:
        loop.create_task(main())
        loop.run_forever()
    finally:
        loop.close()
{% else %}
if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        from rich.console import Console
        c = Console()
        c.print_exception(show_locals=True)
    sys.exit(rc)
{% endif %}

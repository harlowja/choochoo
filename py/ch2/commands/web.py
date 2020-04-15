
import webbrowser
from logging import getLogger

from .args import SUB_COMMAND, SERVICE, STOP, START, STATUS
from ..web.server import WebController


log = getLogger(__name__)


def web(args, system, db):
    '''
## web

    > ch2 web start

Start the web server.

    > ch2 web status

Indicate whether the server is running or not.

    > ch2 web stop

Stop the server.
    '''
    cmd = args[SUB_COMMAND]
    controller = WebController(args, system, db)
    if cmd == SERVICE:
        controller.service()
    elif cmd == STATUS:
        controller.status()
    elif cmd == START:
        controller.start(restart=True)
        webbrowser.open(controller.connection_url(), autoraise=False)
        log.info(controller.connection_url())
    elif cmd == STOP:
        controller.stop()

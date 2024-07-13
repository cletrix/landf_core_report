import tornado.web
import tornado.ioloop
import tornado.autoreload
import asyncio

from tools import *

from views.move import Move
from views.machine import Machine
from views.frontpage import FrontPage
from core.manager import Manager
import constants
import log

from log import logger


def make_app_tornado():
    return tornado.web.Application([
        (r"/", FrontPage),
        (r"/machine", Machine),
        (r"/move", Move),
    ])


async def main():

    clear_terminal()
    log.start(constants.LOG_DIR, constants.LOG_FILE_NAME)
    logger.info(constants.to_str())
    clear_exit()

    app = make_app_tornado()
    await Manager.start()

    tornado.autoreload.start()
    app.listen(constants.PORT)
    await asyncio.Event().wait()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

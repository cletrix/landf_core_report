
import tornado
from log import logger


class FormMachine(tornado.web.RequestHandler):
    def get(self):
        logger.debug('get in maq')

        self.render("form_machine.html")

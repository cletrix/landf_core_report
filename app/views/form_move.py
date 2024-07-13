
import tornado
from log import logger


class FormMove(tornado.web.RequestHandler):
    def get(self):

        self.render("form_move.html")

import time
from typing import Any

import tornado
from tornado import httputil

import constants
from log import logger


class BaseHandler(tornado.web.RequestHandler):
    request_count = 0
    speed = 0.0

    def __init__(self, application: "Application", request: httputil.HTTPServerRequest, **kwargs: Any):
        super().__init__(application, request, **kwargs)
        self.start_time = 0

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Authorization")

    def options(self):
        self.set_status(204)
        self.finish()

    def prepare(self):
        BaseHandler.request_count += 1
        self.start_time = time.time()

    @classmethod
    def reset_request_count(cls):
        cls.speed = cls.request_count/5
        cls.request_count = 0

    def on_finish(self):
        if constants.MODE_ENV == 'LOCAL':
            duration = (time.time() - self.start_time) * 1000
            logger.info(f"took:{duration:.4f}ms from:{self.request.uri} ")

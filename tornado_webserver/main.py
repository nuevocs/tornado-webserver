import tornado.ioloop
import tornado.web
import json
from src import log
from src.constant import PORT

logger = log.logging_func("webhook-server", log.logging.DEBUG)


class WithingsNotify(tornado.web.RequestHandler):
    async def post(self):
        if self.request.headers.get(
                "Content-Type") != "application/x-www-form-urlencoded":  # application/x-www-form-urlencoded
            raise [tornado.web.HTTPError(400),
                   logger.debug(f"Wrong content-type. {self.request.headers}")]
        logger.debug(f"Correct content-type. Here is a response Header. {self.request.headers}")
        data = json.loads(self.request.body)
        logger.debug(f"Here is a received DATA. {data}")
        logger.debug(f"Here is a body {self.request.body}")
        logger.debug(f"Here is a uri {self.request.uri}")
        logger.debug(f"Here is a body arguments {self.request.body_arguments}")
        logger.debug(f"Here is a arg {self.request.arguments}")
        logger.debug(f"Here is a query {self.request.query}")
        logger.debug(f"Here is a query arg {self.request.query_arguments}")


        self.write({'result': 'OK'})

    async def get(self):
        logger.debug(f"received GET request. {self.request.headers}")
        self.write({'result': 'OK'})

    async def head(self):
        logger.debug(f"received HEAD headers. {self.request.headers}")
        logger.debug(f"received HEAD body. {self.request.body}")
        self.write({'result': 'head'})


class CallBackCheck(tornado.web.RequestHandler):
    async def get(self):
        logger.debug(f"received GET headers. {self.request.headers}")
        logger.debug(f"received GET body. {self.request.body}")
        self.write({'result': 'get'})

    async def post(self):
        logger.debug(f"received POST headers. {self.request.headers}")
        logger.debug(f"received POST body. {self.request.body}")
        self.write({'result': 'post'})

    async def head(self):
        logger.debug(f"received HEAD headers. {self.request.headers}")
        logger.debug(f"received HEAD body. {self.request.body}")
        self.write({'result': 'head'})


handlers = [
    (r"/withings", WithingsNotify),
    (r"/callback", CallBackCheck),
]

if __name__ == "__main__":
    application = tornado.web.Application(handlers)
    application.listen(port=PORT, address='0.0.0.0')
    RUNNING = f"Running: 0.0.0.0:{PORT}..."
    print(RUNNING)
    logger.debug(RUNNING)
    tornado.ioloop.IOLoop.current().start()

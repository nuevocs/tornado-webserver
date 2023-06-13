import tornado.ioloop
import tornado.web
import json
import os
from dotenv import load_dotenv
from src import log

load_dotenv()

PORT = int(os.environ["PORT"])
logger = log.logging_func("webhook-server", log.logging.DEBUG)


class WithingsNotify(tornado.web.RequestHandler):
    async def post(self):
        if self.request.headers.get("Content-Type") != "application/x-www-form-urlencoded": # application/x-www-form-urlencoded
            raise [tornado.web.HTTPError(400),
                   logger.debug(f"Wrong content-type. {self.request.headers}")]
        logger.debug(f"Correct content-type. Here is a response Header. {self.request.headers}")
        data = json.loads(self.request.body)
        logger.debug(f"Here is a received DATA. {data}")
        self.write({'result': 'OK'})


handlers = [
    (r"/withings", WithingsNotify),
]

if __name__ == "__main__":
    application = tornado.web.Application(handlers)
    application.listen(port=PORT, address='0.0.0.0')
    RUNNING = f"Running: 0.0.0.0:{PORT}..."
    print(RUNNING)
    logger.debug(RUNNING)
    tornado.ioloop.IOLoop.current().start()

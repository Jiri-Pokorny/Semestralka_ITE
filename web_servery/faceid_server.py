import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.log
from urllib.request import urlopen
import datetime as dt
import logging
from recognize_handler import RecognizeImageHandler


tornado.log.enable_pretty_logging()
app_log = logging.getLogger("tornado.application")


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie("user","")
        self.render("static/index.html")


class ReceiveImageHandler(tornado.web.RequestHandler):
    def post(self):
        # Convert from binary data to string
        received_data = self.request.body.decode()

        assert received_data.startswith("data:image/png"), "Only data:image/png URL supported"

        # Parse data:// URL
        with urlopen(received_data) as response:
            image_data = response.read()

        app_log.info("Received image: %d bytes", len(image_data))

        # Write an image to the file
        with open(f"images/img-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}.png", "wb") as fw:
            fw.write(image_data)


application = tornado.web.Application([
    (r'/', RootHandler),
    (r"/receive_image", ReceiveImageHandler),
    (r"/recognize", RecognizeImageHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static/"}),
], cookie_secret = "QipdponPX/PKV/weDJBxhwXc0YQDIk8Zk3DtVa9ioFeZh0BVJ9Uq4e")

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": "cert.pem",
        "keyfile": "key.pem",
        "ca_certs": "fullchain.pem",
    })
    http_server.listen(443)
    tornado.ioloop.IOLoop.instance().start()

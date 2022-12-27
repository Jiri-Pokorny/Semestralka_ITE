# basic_server.py

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from os.path import join, dirname
import json

class MainHandler(RequestHandler):
    def get(self):
        #if self.get_secure_cookie("name") is None:
        #   self.write("You don't have permission to be here.")
        #   self.redirect("https://sulis150/faceid_server/static/login/index.html")
        self.render("faceid_server/static/login/index.html")


class JsonHandler(RequestHandler):
    def get(self):
        self.write(json.dumps(storage))


class WebApp(Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/json/", JsonHandler),
            ('/(.*)', StaticFileHandler, {'path': join(dirname(__file__), 'faceid_server/static/')})
        ]
        settings = {
            "debug": True
        }
        Application.__init__(self, handlers, **settings, cookie_secret = "QipdponPX/PKV/weDJBxhwXc0YQDIk8Zk3DtVa9ioFeZh0BVJ9Uq4e")


if __name__ == '__main__':
    application = WebApp()
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": "cert.pem",
        "keyfile": "key.pem",
        "ca_certs": "fullchain.pem",
    })
    http_server.listen(55555)
    tornado.ioloop.IOLoop.current().start()
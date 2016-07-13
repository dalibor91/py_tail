import tornado.websocket
import tornado.web
import tornado.ioloop
import tornado.template
import json
import filetail
import func
import threading

class WebSocketHandle(tornado.websocket.WebSocketHandler):

    def initialize(self, data):
        self.configuration = data

    def open(self):
        print("WebSocket connection opened")

    def on_message(self, message):
	func.log("New request: %s" % str(message))
        data = json.loads(message)
        if "file" in data:
            for conf in self.configuration:
                if conf["file"] == data["file"]:
                    self.parser = filetail.FileTail(conf["file"])
                    linenum = 0 if "len" not in data else int(data["len"])
                    self.startTailing(linenum)
                    return None

    def startTailing(self, fromlines):
        self.parser.tailfrom(int(fromlines), self.write_message)

    def check_origin(self, origin):
        return True

    def on_close(self):
        print("WebSocket closed");


class IndexHandle(tornado.web.RequestHandler):
    def initialize(self, data):
        self.configuration = data

    def get(self):
        self.render("public/index.html", data=self.configuration)



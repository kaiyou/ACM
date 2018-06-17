import tornado

from acm import pubsub


__version__ = '1'


broker = pubsub.Broker()


def start():
    from acm import server
    server.app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

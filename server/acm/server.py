from tornado import websocket, web, ioloop
from acm import __version__, broker

import json


class WSHandler(websocket.WebSocketHandler):
    """ Handles the socket implementation of the protocol.
    """

    def check_origin(self, origin):
        """ Connections might be open from anywhere
        """
        return True

    def on_close(self):
        """ Cancel all subscriptions
        """
        pass

    def on_message(self, message):
        """ Handles an incoming message
        """
        print(message)
 

class APIHandler(web.RequestHandler):
    """ Generic request handler that adds a HTTP header.
    """

    def prepare(self):
        self.set_header('X-Acm-Version', __version__)


class IndexHandler(APIHandler):
    """ Return an empty response
    """

    def head(self):
        return


class PollHandler(APIHandler):
    """ Handles the polling HTTP API
    """

    def get(self):
        """ Return the available notifications for the given
        channels, result is presented as a JSON list:

            [
                {"channel": "...",
                 "format": 1,
                 "content": "Mjaiz1Ji"
                },
                ...
            ]
        """
        channel_ids = self.get_arguments('id')
        return json.dumps([
            {'channel': channel,
             'format': format_,
             'content': content}
            for channel, (format_, content) in broker.consume(channel_ids)
        ])


class PubHandler(APIHandler):
    """ Handles the publication HTTP API
    """

    def post(self):
        """ Publish a new notification, parameters must
        be posted in a JSON body:

            {"channel": "...",
             "format": 1,
             "content": "Mjaiz1Ji"
            }
        """
        print(self.get_body())


app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', WSHandler),
    (r'/poll', PollHandler),
    (r'/pub', PubHandler),
])



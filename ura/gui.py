import traceback

import eventlet
import socketio

from .src import init  # type: ignore
from .src.download import Downloader
from .src.settings import cfg, wr_cfg

sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


class Exp:
    def config(sid, *args, **kwargs):
        try:
            return True, cfg(None)
        except Exception:
            return False, traceback.format_exc()

    def write_config(sid, stg, value):
        try:
            wr_cfg(stg, value)
            return True, None
        except Exception:
            return False, traceback.format_exc()

    def dl(sid, url):
        try:
            return True, Downloader().dlch(url)
        except Exception:
            return False, traceback.format_exc()


for i in [f for f in dir(Exp) if callable(getattr(Exp, f)) and not f.startswith("__")]:
    sio.on(i, getattr(Exp, i))

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 9173)), app)

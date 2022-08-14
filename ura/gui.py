import traceback
from typing import Any, Callable

import eventlet
import socketio

from .src import init  # type: ignore
from .src.cfg import de_rcfg, de_wcfg
from .src.download import Downloader
from .src.globals import CFG_PATH

sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print("c0VjUmVUX2NPZEUgYnkgd2hpX25l: Connected")


@sio.event
def connect_error(data):
    print("Connection failed.")


@sio.event
def disconnect(sid):
    print("Disconnected")


def texc(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return False, "\n    ".join(traceback.format_exc().split("\n"))

    return inner


class Expose:
    @texc
    def cfg_path(*args, **kwargs):
        return True, CFG_PATH

    @texc
    def config(*args, **kwargs):
        return True, de_rcfg()

    @texc
    def write_config(sid, stg, value):
        op = de_rcfg()
        op.modify(stg, value)
        de_wcfg(op)
        return True, None

    @texc
    def dl(sid, url):
        return True, Downloader().dlch(url)


expose = []

for i in dir(Expose):
    if callable(getattr(Expose, i)) and not i.startswith("__"):
        expose.append(i)

for i in expose:
    sio.on(i, getattr(Expose, i))

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 9173)), app)

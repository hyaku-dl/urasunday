import inspect
import traceback
from datetime import datetime
from typing import Any, Callable

import eventlet
import socketio

try:
    from src import init  # type: ignore
    from src import __version__, cholder
    from src.cfg import de_rcfg, de_wcfg
    from src.download import Downloader
    from src.globals import CFG_PATH
except ImportError:
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


@sio.on("log_path")
def log_path_fn(sid, data):
    global log_path
    log_path = data
    return True, None


@sio.on("log")
def log(name: str, *msg) -> None:
    """Log message to console.

    Args:
        msg (str): Message to be logged.
    """
    if len(msg) == 1:
        msg = msg[0]
    else:
        msg = " ".join(msg)
    op = "[{}] {}: {}\n".format(
        datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"),
        name,
        msg,
    )
    print(op)
    with open(log_path, "a") as f:
        f.write(op)

    return True, None


@sio.on("log")
def exp_log(sid, name: str, *msg) -> None:
    return True, log(name, msg)


def tex(func: Callable[[Any], Any]) -> Callable[[Any], tuple[bool, Any]]:
    """Try except wrapper

    Args:
        func (Callable[[Any], Any]): Function to be wrapped.

    Returns:
        Callable[[Any], Any]: Wrapped function.
    """

    def inner(*args, **kwargs) -> tuple[bool, Any]:
        """If function raises an exception, return a tuple consisting of False and the exception message.

        Returns:
            tuple[bool, Any]: err, res.
        """
        try:
            op = func(*args, **kwargs)
        except Exception as e:
            op = False, "\n    ".join(traceback.format_exc().strip().split("\n"))
        for i in op:
            log(func.__name__, i)
        return op

    return inner


def rta(func: Callable[[Any], Any]) -> Callable[[Any], tuple[True, Any]]:
    """Return True, Any

    Args:
        func (Callable[[Any], Any]): Function to be wrapped.

    Returns:
        Callable[[Any], tuple[True, Any]]: Wrapped function.
    """

    def inner(*args, **kwargs):
        return True, func(*args, **kwargs)

    inner.__name__ = func.__name__
    return inner


def rbn(func: Callable[[Any], bool]) -> Callable[[Any], tuple[bool, None]]:
    """Return bool, None

    Args:
        func (Callable[[Any], bool]): Function to be wrapped.

    Returns:
        Callable[[Any], tuple[bool, None]]: Wrapped function.
    """

    def inner(*args, **kwargs):
        return func(*args, **kwargs), None

    inner.__name__ = func.__name__
    return inner


def rtn(func: Callable[[Any], None]) -> Callable[[Any], tuple[True, None]]:
    """Return True, None

    Args:
        func (Callable[[Any], None]): Function to be wrapped.

    Returns:
        Callable[[Any], tuple[True, None]]: Wrapped function.
    """

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        return True, None

    inner.__name__ = func.__name__
    return inner


class Expose:
    @rta
    def info(*args, **kwargs) -> dict[str, str]:
        op = {
            "cfg_path": CFG_PATH,
            "cholder": cholder,
            "version": __version__,
        }
        return op

    @rta
    def config(*args, **kwargs) -> dict[str, Any]:
        return de_rcfg()

    @rtn
    def write_config(sid, stg, value) -> None:
        op = de_rcfg()
        op.modify(stg, value)
        de_wcfg(op)

    @rta
    def dl(sid, url) -> str:
        return Downloader().dlch(url)


expose = []

for i in dir(Expose):
    ifn = getattr(Expose, i)
    if callable(ifn) and not i.startswith("__"):
        sio.on(i, tex(ifn))

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 9173)), app)

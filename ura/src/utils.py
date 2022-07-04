import ast
import itertools
import re
import sys
import unicodedata
from datetime import datetime, timedelta
from functools import lru_cache
from os.path import dirname as dn
from os.path import realpath as rp
from time import strftime, strptime
from typing import Any

import arrow

# https://stackoverflow.com/a/93029
ALL_CHARS = (chr(i) for i in range(sys.maxunicode))
CATEGORIES = {'Cn'}
CCHARS = ''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0))))
CCHARS_RE = re.compile('[%s]' % re.escape(CCHARS))

def sanitize_text(s: str):
    return unicodedata.normalize("NFKD", CCHARS_RE.sub('', s)).strip()

def dnrp(file: str, n: int=1) -> str:
    """
    Get the directory component of a pathname by n times recursively then return it.

    Args:
        file (str): File to get the directory of.
        n (int, optional): Number of times to get up the directory???? Defaults to 1.

    Returns:
        op (str): The directory component got recursively by n times from the given pathname
    """
    op = rp(file)
    for _ in range(n):
        op = dn(op)
    return op

def de(a: Any, d: Any) -> Any:
    """
    Defaults. Return a if a is True, else returns d.

    Args:
        a (Any): Object to be tested, will be returned if evaluates to True.
        d (Any): Default object to be returned if `a` evaluates to False.

    Returns:
        Any
    """
    if a:
        return a
    else:
        return d

def dd(default: dict[Any, Any], d: dict[Any, Any] | None) -> dict[Any, Any]:
    """
    Defaults dictionary. Overwrite the items in the default dict with the
    items in the d dict.

    Args:
        default (Dict[Any, Any]): The dict to rewrite the items to.
        d (Union[Dict[Any, Any], None]): The dict to rewrite the items from.

    Returns:
        dict[Any, Any]
    """
    op = default
    if d:
        for a, v in d.items():
            op[a] = v
    return op

def ddir(d: dict[Any, Any], dir: str, de: Any={}) -> Any:
    """
    Retrieve dictionary value using recursive indexing with a string.
    ex.:
        `ddir({"data": {"attr": {"ch": 1}}}, "data/attr/ch")`
        will return `1`


    Args:
        dict (dict): Dictionary to retrieve the value from.
        dir (str): Directory of the value to be retrieved.

    Returns:
        op (Any): Retrieved value.
    """
    op = d
    for a in dir.split("/"):
        op = op[a]
    return op or de

def dpop(
    d: dict[Any, Any],
    pop: list[int | tuple[str | int | tuple] | str],
    de: Any=None
) -> Any:
    """
    Iterate through the preferred order of precedence (`pop`) and see if
    the value exists in the dictionary. If it does, return it. If not, return
    `de`.

    Args:
        d (Dict[Any, Any]): Dictionary to retrieve the value from.
        pop (list[int | tuple[str | int | tuple]  |  str]): List of keys to
            iterate through.
        de (Any, optional): Default object to be returned. Defaults to None.

    Returns:
        Any: Retrieved value.
    """

    for i in pop:
        if op:= d.get(i):
            return op
    return de

@lru_cache
def dt(dt: str, format: str) -> str:
    """
    Remove timezone from datetime and format it to ISO 8601 format.

    Args:
        dt (str): Unformatted datetime string to be formatted to ISO 8601 format
        format (str): The initial format of the datetime string

    Returns:
        str: Formatted datetime string
    """

    op = dt
    if "ago" in dt and not format:
        arw = arrow.utcnow()
        op = arw.dehumanize(dt)
    tz = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([-+])(\d{2}):(\d{2})", op)
    if tz:
        iso, s, ho, mo = tz.groups()
        s = -1 if s == "-" else 1
        op = (datetime.fromisoformat(iso) - (s * timedelta(hours=int(ho), minutes=int(mo)))).strftime("%Y-%m-%dT%H:%M:%S")
    else:
        op = strftime("%Y-%m-%dT%H:%M:%S", strptime(dt, format))
    return op

@lru_cache
def dt_ts(ts: str) -> str:
    """
    Convert the given unix timestamp to ISO 8601 format.

    Args:
        ts (str): unix timestamp to be converted to ISO 8601 format

    Returns:
        str: Formatted datetime string
    """

    return (datetime.utcfromtimestamp(int(ts))).strftime("%Y-%m-%dT%H:%M:%S")

def le(expr: str) -> Any:
    return ast.literal_eval(expr) if expr else expr

def dnrp(file: str, n: int=1) -> str:
    """
    Get the directory component of a pathname by n times recursively then return it.

    Args:
        file (str): File to get the directory of.
        n (int, optional): Number of times to get up the directory???? Defaults to 1.

    Returns:
        op (str): The directory component got recursively by n times from the given pathname
    """
    op = rp(file)
    for _ in range(n):
        op = dn(op)
    return op
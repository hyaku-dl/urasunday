import ast
import itertools
import re
import shlex
import sys
import unicodedata
from datetime import datetime, timedelta
from functools import lru_cache
from os import makedirs, path
from os.path import dirname as dn
from os.path import realpath as rp
from subprocess import call
from time import strftime, strptime
from typing import Any

import arrow

# Constants
CATEGORIES = {"Cn"}
PR = ["alpha", "beta", "rc"]

# Derived Constants
ALL_CHARS = (chr(i) for i in range(sys.maxunicode))
CCHARS = "".join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7F, 0xA0))))
CCHARS_RE = re.compile("[%s]" % re.escape(CCHARS))

# Functions
def inmd(p: str, ls: list[str] = None) -> str:
    """ "If Not `path.isdir`, Make Directories"

    Args:
    - p (`str`): The path to be created, if it does not exist.

    Returns:
    `str`: The path given.
    """

    pd = path.dirname(p)
    if (pd) and (not path.isdir(pd)):
        makedirs(pd)
        if ls:
            ls.append(pd)
    return p


def ivnd(var: Any, de: Any) -> Any:
    """If Var is None, return Default else var.

    Args:
    - var (`Any`): Variable to check if it is None.
    - de (`Any`): Default value to return if var is None.

    Returns:
    `Any`: var if var is not None else de.
    """
    if var is None:
        return de
    return var


def dnrp(file: str, n: int = 1) -> str:
    """
    Get the directory component of a pathname by n times recursively then return it.

    Args:
    - file (`str`): File to get the directory of.
    - n (`int`, optional): Number of times to get up the directory???? Defaults to 1.

    Returns:
    `str`: The directory component got recursively by n times from the given pathname
    """
    op = rp(file)
    for _ in range(n):
        op = dn(op)
    return op


def dpop(
    d: dict[Any, Any], pop: list[int | tuple[str | int | tuple] | str], de: Any = None
) -> Any:
    """Iterate through the preferred order of precedence (`pop`) and see if the value exists in the dictionary. If it does, return it. If not, return `de`.

    Args:
    - d (`Dict[Any, Any]`): Dictionary to retrieve the value from.
    - pop (`list[int | tuple[str | int | tuple] | str]`): List of keys to iterate through.
    - de (`Any`, optional): Default object to be returned. Defaults to None.

    Returns:
    `Any`: Retrieved value.
    """

    for i in pop:
        if op := d.get(i):
            return op
    return de


@lru_cache
def dt(dt: str, format: str) -> str:
    """Remove timezone from datetime and format it to ISO 8601 format.

    Args:
    - dt (`str`): Unformatted datetime string to be formatted to ISO 8601 format
    - format (`str`): The initial format of the datetime string

    Returns:
    `str`: Formatted datetime string
    """

    op = dt
    if "ago" in dt and not format:
        arw = arrow.utcnow()
        op = arw.dehumanize(dt)
    tz = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([-+])(\d{2}):(\d{2})", op)
    if tz:
        iso, s, ho, mo = tz.groups()
        s = -1 if s == "-" else 1
        op = (
            datetime.fromisoformat(iso)
            - (s * timedelta(hours=int(ho), minutes=int(mo)))
        ).strftime("%Y-%m-%dT%H:%M:%S")
    else:
        op = strftime("%Y-%m-%dT%H:%M:%S", strptime(dt, format))
    return op


@lru_cache
def dt_ts(ts: str) -> str:
    """Convert the given unix timestamp to ISO 8601 format.

    Args:
        ts (str): unix timestamp to be converted to ISO 8601 format

    Returns:
        str: Formatted datetime string
    """

    return (datetime.utcfromtimestamp(int(ts))).strftime("%Y-%m-%dT%H:%M:%S")


def le(expr: str) -> Any:
    return ast.literal_eval(expr) if expr else expr


def repl(s: str, repl_dict: dict[str, list[str]]) -> str:
    op = s
    for k, v in repl_dict.items():
        for i in v:
            op = op.replace(i, k)
    return op


def run(s: str):
    call(shlex.split(s))


# https://stackoverflow.com/a/93029
def sanitize_text(s: str):
    return unicodedata.normalize("NFKD", CCHARS_RE.sub("", s)).strip()

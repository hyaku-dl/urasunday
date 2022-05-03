import shlex
from os import makedirs, path
from subprocess import call
from typing import Any

from mako.lookup import TemplateLookup

from .settings import stg

YAHML = stg(None, "dev.yml")

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
        op = op.get(a)
        if not op:
            break
    return op or de

LOOKUPS = TemplateLookup(directories=ddir(YAHML, "file/templates") or [])

def srv_tpl(tn: str, lookup: TemplateLookup=LOOKUPS, **kwargs: dict[str, Any]):
    return lookup.get_template(tn).render(**kwargs)

def run(s: str):
    call(shlex.split(s))

def repl(s: str, repl_dict: dict[str, list[str]]) -> str:
    op = s
    for k, v in repl_dict.items():
        for i in v:
            op = op.replace(i, k)
    return op

def inmd(p: str, ls: list[str]=None):
    """
    "If Not `path.isdir`, Make Directories"

    Args:
        p (str): [description]
    """

    pd = path.dirname(p)
    if (pd) and (not path.isdir(pd)):
        makedirs(pd)
        if ls:
            ls.append(pd)
    return p
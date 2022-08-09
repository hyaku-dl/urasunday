import shlex
from os import makedirs, path
from subprocess import call
from typing import Any

# Constants

PR = ["alpha", "beta", "rc"]

# Functions
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

def ivnd(var: Any, de: Any) -> Any:
    """If Var is None, return Default else var.

    Args:
        var (Any): Variable to check if it is None.
        de (Any): Default value to return if var is None.

    Returns:
        Any: var if var is not None else de.
    """
    if var is None:
        return de
    return var

def repl(s: str, repl_dict: dict[str, list[str]]) -> str:
    op = s
    for k, v in repl_dict.items():
        for i in v:
            op = op.replace(i, k)
    return op

def run(s: str):
    call(shlex.split(s))
import os
from os import path
from os.path import abspath as ap
from os.path import dirname as dn
from typing import Any, Dict

import msgpack
import yaml

from ura.globals import CFLOP


def readcfg(file: str) -> Any:
    """Read the contents of a file with the given file name.

    Args:
        file (str): File name of the file to read the contents of.

    Returns:
        Any: The contents of the file.
    """

    match file.split(".")[-1]:
        case "yml":
            with open(file, "r") as f:
                return yaml.safe_load(f.read())
        case "mp":
            with open(file, "rb") as f:
                return msgpack.unpackb(f.read(), raw=False, use_list=True)

def stg(stg: str, file: str = path.join(dn(ap(__file__)), "stg.json")) -> Any:
    """Retrieve dictionary value of the config file with the given file name
    using recursive indexing with a string.
    ex.:
        Given that settings.json contains: `{"data": {"attr": {"ch": 1}}}`
        `stg("data/attr/ch", "settings.json")` will return `1`

    Args:
        stg (str): Directory of the value to be retrieved.
        file (str, optional): File name of the file to get the value from. Defaults to `path.join(dn(ap(__file__)), "settings.json")`.

    Returns:
        Any: The retrieved value.
    """
    op = readcfg(file)
    if stg is not None:
        for a in stg.split("/"):
            op = op[a]
    return op


def wr_stg(stg: str, value: Any, file: str = path.join(dn(ap(__file__)), "stg.json")) -> None:
    """Rewrite dictionary value of the config file with the given file name
    using recursive indexing with a string.
    ex.:
        Given that settings.json contains: `{"data": {"attr": {"ch": 1}}}`
        `wr_stg("data/attr/ch", 2)`
        will rewrite settings.json to be: `{"data": {"attr": {"ch": 2}}}`

    Args:
        stg (str): Directory of the value to be rewrited.
        value (Any): Value to rewrite to.
        file (str, optional): File name of the file to rewrite the value from. Defaults to path.join(dn(ap(__file__)), "settings.json").

    Raises:
        FileNotFoundError: Raised if the file is not found.
    """

    def _write(stg_dict: dict[any, any]) -> None:
        match file.split(".")[-1]:
            case "yml":
                with open(file, "w") as f:
                    yaml.dump(stg_dict, f, indent=4)
            case "mp":
                with open(file, "wb") as f:
                    f.write(msgpack.packb(stg_dict, use_bin_type=True))

    def _modify(stg: str, value: Any, stg_dict: Dict[Any, Any]):
        path_ls = stg.split("/")
        key = path_ls[0]
        if len(path_ls) > 1:
            try:
                stg_dict[key]
            except KeyError:
                stg_dict[key] = {}
            if isinstance(stg_dict[key], dict):
                _modify(stg.replace(f"{key}/", ""), value, stg_dict[key])
            else:
                f_stg = '"]["'.join(stg.split("/"))
                raise FileNotFoundError(f'["{f_stg}"] at {file} not found.')
        else:
            stg_dict[key] = value
            return stg_dict

    if os.path.exists(file) and stg:
        stg_dict = readcfg(file)
        _modify(stg, value, stg_dict)
        _write(stg_dict)
    else:
        _write(value)

def cfg_path() -> str:
    for i in CFLOP:
        if os.path.exists(str(i)):
            config_path = i
            break
    return config_path

def cfg(*args, **kwargs) -> Any:
    return stg(*args, cfg_path(), **kwargs)
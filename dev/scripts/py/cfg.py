import json
from typing import Any

import msgpack
import yaml

from .cd import CustomDict
from .exceptions import c_exc_str

TYPES = {
    "r": [
        [["yaml", "yml"], ["r", lambda x: yaml.safe_load(x)]],
        [["mp"], ["rb", lambda x: msgpack.unpackb(x, raw=False, use_list=True)]],
        [["json"], ["r", lambda x: json.loads(x)]],
    ],
    "w": [
        [["yaml", "yml"], ["w", lambda x: yaml.dump(x, indent=2)]],
        [["mp"], ["wb", lambda x: msgpack.packb(x, use_bin_type=True)]],
        [["json"], ["w", lambda x: json.dumps(x, indent=4, sort_keys=False)]],
    ],
}


@c_exc_str
class ExtensionNotSupported(NotImplementedError):
    def __init__(self, ext: str) -> None:
        self.message = f"Extension `{ext}` is not supported."
        super().__init__(self.message)


def pcfg(d: str, type: str) -> CustomDict:
    """Parse the given string as the given type.

    Args:
        d (str): String to parse.
        type (str): Type to parse the string as.

    Returns:
        CustomDict: The parsed string.
    """

    for k, v in TYPES["r"]:
        if type in k:
            return CustomDict(v[1](d))
    raise ExtensionNotSupported(type)


def dcfg(value: dict, ext: str) -> str:
    """Dump the given value to a string with the given extension.

    Args:
        value (dict): Value to dump to a string.
        ext (str): Extension to dump the value to.

    Returns:
        str: The dumped value.
    """

    for k, v in TYPES["w"]:
        if ext in k:
            return v[1](value)
    raise ExtensionNotSupported(ext)


def rcfg(file: str) -> CustomDict:
    """Read the contents of a file with the given file name.

    Args:
        file (str): File name of the file to read the contents of.

    Returns:
        CustomDict: The contents of the file.
    """

    ext = file.split(".")[-1]
    for k, v in TYPES["r"]:
        if ext in k:
            with open(file, v[0]) as f:
                return CustomDict(v[1](f.read()))
    raise ExtensionNotSupported(ext)


def wcfg(file: str, value: dict[Any, Any] | list[Any]) -> None:
    """Write the given value to a file with the given file name.

    Args:
        file (str): File name of the file to write the value to.
        value (dict[Any, Any] | list[Any]): Value to write to the file.
    """
    ext = file.split(".")[-1]
    for k, v in TYPES["w"]:
        if ext in k:
            with open(file, v[0]) as f:
                if value.__class__.__mro__[-2] is dict:
                    value = dict(value)
                f.write(v[1](value))

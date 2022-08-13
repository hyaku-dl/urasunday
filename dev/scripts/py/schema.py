import re
from os import path
from os.path import abspath as ap

from .cfg import wcfg
from .exceptions import c_exc_str
from .utils import dnn

# Constants
TD = {
    "str": "",
    "int": -1,
    "float": -1.0,
    "bool": False,
    "list": [],
    "dict": {},
}

# Derived Constants
UT_RE = re.compile(r"(\w+)(?:\[)?")
UT = lambda x: UT_RE.match(x).group(1)


@c_exc_str
class VersionNotFound(ValueError):
    def __init__(self, name: str, v: str):
        self.name = name
        self.v = v
        self.msg = f"Version {v} not found in {name}"


def __init__(self, v: str):
    try:
        self.u, self.d, *_ = v.split(".")
    except AttributeError:
        raise VersionNotFound(self.__name__, v)


def __call__(self, *args, **kwargs):
    return getattr(getattr(self, f"u{self.u}"), f"d{self.d}")(*args, **kwargs)


def c_schema(cls: object) -> object:
    cls.__init__ = __init__
    cls.__call__ = __call__
    return cls


@c_schema
class Schema:
    class u1:
        def d0(yml: dict[str, dict[str, str | int | float]]):
            content = ""
            for k, v in yml.items():
                content += f"## **{k}**"
                for vk, vv in v.items():
                    content += f'\n\n- ### **{vk}**\n\n\t`{vv["type"]}`'
                    if de := vv.get("default", None):
                        content += f", defaults to `{de}`"
                    if abbr := vv.get("abbr", None):
                        content += f"\n\n\t*{abbr}*"
                    content += "\n\n\t{}".format(vv["desc"].replace("\n", "\n\t"))
            return content.replace("\t", "    ")


@c_schema
class Config:
    class u1:
        def d0(yml: dict[str, dict[str, str | int | float]]):
            op = {}
            for k, v in yml.items():
                op[k] = v.get("default", TD.get(UT(v["type"]), None))
            wcfg(path.join(dnn(ap(__file__), 4), "ura/src/cf_tpl.mp"), op)

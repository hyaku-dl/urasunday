from os import path
from os.path import abspath as ap
from os.path import dirname as dn

from scripts.settings import wr_stg


class Config:
    def v1_0_0(yml: dict[str, dict[str, str | int | float]]):
        op = {}
        for k, v in yml.items():
            if de:=v.get("default", None):
                op[k] = de
            else:
                match v["type"]:
                    case "str":
                        op[k] = ""
                    case "int":
                        op[k] = -1
                    case "float":
                        op[k] = -1.0
                    case "bool":
                        op[k] = False
                    case "list":
                        op[k] = []
                    case "dict":
                        op[k] = {}
        wr_stg(None, op, path.join(dn(dn(ap(__file__))), "ura", "cf_tpl.mp"))

def config(v: str):
    return getattr(Config, f'v{v.replace(".", "_")}')
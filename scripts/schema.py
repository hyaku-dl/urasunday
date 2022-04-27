from os import makedirs, path
from os.path import abspath as ap
from os.path import dirname as dn
from pathlib import Path
from shutil import rmtree

import msgpack
import yaml
from mako.lookup import TemplateLookup

from scripts.settings import wr_stg

from .utils import srv_tpl


def ddir(d: dict[any, any], dir: str) -> any:
    """Retrieve dictionary value using recursive indexing with a string.
    ex.:
        `ddir({"data": {"attr": {"ch": 1}}}, "data/attr/ch")`
        will return `1`

    Args:
        dict (dict): Dictionary to retrieve the value from.
        dir (str): Directory of the value to be retrieved.

    Returns:
        op (any): Retrieved value.
    """
    op = d
    for a in dir.split("/"):
        op = op[a]
    return op

def main():
    with open("./version", "rb") as f:
        vls = msgpack.unpackb(f.read(), raw=False, use_list=False)
    with open(
        path.join("constants", *[str(_) for _ in vls[0:2]], "schema.yml"), "r"
    ) as f:
        schema = yaml.safe_load(f)
    with open("hyaku/schema", "wb") as f:
        f.write(msgpack.packb(schema, use_bin_type=True))
    for i in list(Path("./constants").glob("*/schema.mako")):
        old_path = i.parent
        new_path = path.join("docs", i.parts[-2])
        name = i.stem
        rmtree("docs")
        makedirs(new_path)
        with open(path.join(new_path, f'{name}.md'), 'w') as f, open(path.join(old_path, 'schema.yml'), 'r') as yml:
            f.write(
                srv_tpl(
                    str(i.name),
                    TemplateLookup(directories=[str(old_path)]),
                    **{
                        "yml": yaml.safe_load(yml.read()),
                    }
                )
            )

class Schema:
    def v1_0_0(yml: dict[str, dict[str, str | int | float]]):
        content = ""
        for k, v in yml.items():
            content += f'## **{k}**'
            for vk, vv in v.items():
                content += f'\n\n- ### **{vk}**\n\n\t`{vv["type"]}`'
                if de:=vv.get("default", None):
                    content += f', defaults to `{de}`'
                if abbr:=vv.get("abbr", None):
                    content += f'\n\n\t*{abbr}*'
                content += '\n\n\t{}'.format(vv["desc"].replace("\n", "\n\t"))
        return content.replace("\t", "    ")

def schema(v: str):
    return getattr(Schema, f'v{v.replace(".", "_")}')

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
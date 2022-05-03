import itertools
import re

import ura

from .settings import stg
from .utils import ddir, inmd

RE_MX = r"(?<=\{matrix.)[a-zA-Z0-9-_]+?(?=\})"

SCRIPTS = stg(None, "scripts.yml")
MD_VARS = stg("md_vars", "dev.yml")

MATRIX = {}
for k, v in SCRIPTS["matrix"].items():
    MATRIX[k] = [str(i) for i in v]

with open("requirements.txt", "r") as f:
    REQ = f.read().split("\n")

PG = {
    "req": [i for i in REQ if i],
    "ver": ura.__version__,
    "prerel": not ura.vls[-2] == 3,
}
GLOBAL = {}
for k, v in dict(
    MD_VARS["global"],
    **SCRIPTS["variables"]["global"],
    **PG
).items():
    GLOBAL[k] = str(v)

PL = {
    "req": [i for i in REQ if i],
}
LOCAL = {}
for k, v in dict(
    MD_VARS["local"],
    **SCRIPTS["variables"]["local"],
    **PL
).items():
    LOCAL[k] = str(v)

def cd(*k: list[str]):
    op = []
    dls = [MATRIX[i] for i in k]
    for i in itertools.product(*dls):
        op.append(dict(zip(k, i)))
    return op

def repl(key: str, fn: str, contents: str):
    s, c = fn, contents
    lv = ddir(SCRIPTS, f"variables/local/{key}")
    rmvg = {**GLOBAL, **lv}

    for k, v in rmvg.items():
        c = c.replace(f"${{{k}}}", v)
        s = s.replace(f"${{{k}}}", v)

    return s, c

def mr(k: str, v: dict[str, str]):
    s, c = repl(k, v["path"], v["contents"])
    if mx_match:=re.findall(RE_MX, s):
        op = []
        for i in cd(*mx_match):
            _s = s
            _c = c
            for k, v in i.items():
                _s = _s.replace(f"${{matrix.{k}}}", v)
                _c = _c.replace(f"${{matrix.{k}}}", v)
            op.append([_s, _c])
        return op
    else:
        return [[s, c]]

def main():
    for k, v in SCRIPTS["scripts"].items():
        for p, c in mr(k, v):
            with open(inmd(p), "w") as f:
                f.write(c)
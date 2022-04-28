import os
import shutil
from os import makedirs, path
from pathlib import Path
from typing import Any, Dict, List

import pdoc

from . import schema
from .settings import stg, wr_stg
from .utils import ddir, stg

YML = stg(None, "dev.yml")

DOCS = ddir(YML, "docs")
RULES = ddir(YML, "rules")
IDF = Path(f'./{ddir(YML, "docs/input")}')
MD_VARS_YML = ddir(YML, "md_vars")
RMVC = ddir(MD_VARS_YML, "global")

PDOC = ddir(YML, "pdoc")

CONTEXT = pdoc.Context()
PROJECT = pdoc.Module(PDOC["project"], context=CONTEXT)
pdoc.link_inheritance(CONTEXT)

DGD = []
DGF = []

PGD = []
PGF = []

GEN = {
    "docs": [DGD, DGF],
    "pdoc": [PGD, PGF],
}

class Constants:
    pass

def dd(od: Dict[str, List[str]], *dicts: List[Dict[str, List[str]]]) -> Dict[str, List[str]]:
    for d in dicts:
        for a, v in d.items():
            od[a] = [*(od.get(a, []) or []), *v]
    return od

def rules_fn(rules: Dict[Any, Any]) -> Dict[str, List[str]]:
    return dd({"": ddir(rules, "del", [])}, ddir(rules, "repl"))

def repl(s: str, repl_dict: Dict[str, List[str]]) -> str:
    op = s
    for k, v in repl_dict.items():
        for i in v:
            op = op.replace(i, k)
    return op

def inmd(p: str, type: str):
    """
    "If Not `path.isdir`, Make Directories"

    Args:
        p (str): [description]
    """

    pd = path.dirname(p)
    if not path.isdir(pd):
        GEN[type][0].append(pd)
        makedirs(pd)
    return p

def docs_dir(mn: str, absolute: bool=True) -> str:
    mls = mn.split(".")
    if (len(mls) == 1) and (PDOC["project"] == mls[0]):
        mls[0] = "index"
    elif (len(mls) >= 2) and (PDOC["project"] == mls[0]):
        # mls[0] = "docs"
        del mls[0]
    rel = path.join(*mls[:-1], f"{mls[-1]}.md")
    abs = path.join(PDOC["op"], "docs", rel)
    GEN["pdoc"][1].append(abs)
    inmd(abs, "pdoc")
    if absolute:
        return abs
    else:
        return rel

def yield_text(mod):
    yield mod.name, mod.text()
    sm = {}
    for submod in mod.submodules():
        sm[submod.name] = docs_dir(submod.name, False)
        yield from yield_text(submod)

    if sm:
        if sum:=mod.supermodule:
            sum = f"\n\n## Super-module\n- [{sum.name}]({docs_dir(sum.name, False)})\n"
        else:
            sum = ""

        smls = []
        for k, v in sm.items():
            smls.append(f"- [{k}]({v})")
        sm = "\n\n## Sub-modules\n{}".format("\n".join(smls))

        idx = """# {}{}{}""".format(
            mod.name,
            sum,
            sm,
        )

        idx_path = docs_dir(mod.name)
        with open(idx_path, "w") as f:
            f.write(idx)

def main(rmv: Dict[Any, Any]={}):
    docs_pdir = DOCS["op"]
    rmv_r = ddir(rmv, "rules")
    rmv_mv = ddir(rmv, "md_vars")
    MVC = dict(RMVC, **ddir(rmv_mv, "global"))

    for _, v in stg("generated", "docs/_meta.yml").items():
        for i in v["folders"]:
            if path.isdir(i):
                shutil.rmtree(i)
        for i in v["files"]:
            if path.isfile(i):
                os.remove(i)

    for rip in list(IDF.rglob("*.ymd")):
        out = path.join(
            docs_pdir,
            *rip.parts[1:-1],
            f"{rip.stem}.md"
        )
        print(out)
        GEN["docs"][1].append(out)

        with open(rip, "r") as f:
            md = repl(f.read(), dd(rules_fn(RULES), rules_fn(rmv_r)))

        d = dict(
            MVC,
            **ddir(
                MD_VARS_YML,
                f"local/{rip.stem}"
            ),
            **ddir(
                rmv_mv,
                f"local/{rip.stem}"
            )
        )
        for k, v in d.items():
            md = md.replace(f"${{{k}}}", v)

        with open(inmd(out, "docs"), "w") as f:
            f.write(md)

    for module_name, html in yield_text(PROJECT):
        _dd = docs_dir(module_name)
        with open(_dd, "w") as f:
            f.write(html)
        GEN["pdoc"][1].append(_dd)

    for k, v in GEN.items():
        for key, i in zip(["folders", "files"], v):
            wr_stg(f"generated/{k}/{key}", list(set(i)), "docs/_meta.yml")
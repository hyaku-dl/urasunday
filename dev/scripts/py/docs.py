import os
import re
import shutil
from os import listdir, path
from os.path import dirname as dn
from pathlib import Path
from typing import Any, Dict, List

import frontmatter
import pdoc
import yaml
from mako.template import Template

from .cfg import rcfg, wcfg
from .md_vars import VYML, YML
from .utils import inmd, repl, run

# Constants
RE_MDSE = r"(?<=# {key} start\n).+(?=\n\s*# {key} end)"

# Derived Constants
VLS = VYML["ls"]

PDOC = YML["pdoc"]
MAKO = YML["mako"]
DOCS = YML["docs"]

IDF = Path(DOCS["input"])

CONTEXT = pdoc.Context()
PROJECT = pdoc.Module(PDOC["project"], context=CONTEXT)
pdoc.link_inheritance(CONTEXT)
pdoc.tpl_lookup = pdoc.TemplateLookup(directories=[PDOC["tpl"]])


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)

# Initialization
GEN = {
    "docs": [[], []],
    "mako": [[], []],
    "pdoc": [[], []],
}


class Constants:
    pass


def dd(
    od: Dict[str, List[str]], *dicts: List[Dict[str, List[str]]]
) -> Dict[str, List[str]]:
    for d in dicts:
        for a, v in d.items():
            od[a] = [*(od.get(a, []) or []), *v]
    return od


def rules_fn(rules: Dict[Any, Any]) -> Dict[str, List[str]]:
    return dd({"": rules.get("del", [])}, rules["repl"])


def docs_dir(mn: str, absolute: bool = True, api=False) -> str:
    mls = mn.split(".")
    if (len(mls) == 1) and (PDOC["project"] == mls[0]):
        mls[0] = "index"
    elif (len(mls) >= 2) and (PDOC["project"] == mls[0]):
        del mls[0]
    rel_ls = [*[str(i) for i in VLS[0:2]], *mls[:-1], f"{mls[-1]}.md"]
    if api:
        rel_ls.insert(2, "api")
        rel_ls.insert(0, "docs")
    rel = path.join(*rel_ls)
    abs = path.join(PDOC["op"], rel)
    GEN["pdoc"][1].append(abs)
    inmd(abs, GEN["pdoc"][0])
    if absolute:
        return abs
    else:
        return rel


def yield_text(mod):
    yield mod.name, mod.text()
    sm = {}
    for submod in mod.submodules():
        sm[submod.name] = docs_dir(submod.name, api=True)
        yield from yield_text(submod)

    if sm:
        header = []
        m, *ls = mod.name.split(".")
        for idx, i in enumerate(ls[::-1]):
            header.append(f'[{i}]({"../" * idx}{i}.md)')
        header = ".".join(
            [f"[{m}](" + "../" * (len(ls) - 1) + "index.md)"] + header[::-1]
        )

        if sum := mod.supermodule:
            docs_dir(sum.name, api=True)
            sum = f'\n\n## **<a href="#super" id="super">Super-module</a>**\n- [{sum.name}](index.md)\n'
        else:
            sum = ""

        smls = []
        for k, v in sm.items():
            v = "/".join(v.split("/")[5:])
            smls.append(f"- [{k}]({v})")
        sm = '\n\n## **<a href="#sub" id="sub">Sub-modules</a>**\n\n{}\n'.format(
            "\n".join(smls)
        )

        idx = """# **{}**{}{}""".format(
            header,
            sum,
            sm,
        )

        idx_path = docs_dir(mod.name, api=True)
        with open(idx_path, "w") as f:
            f.write(idx)


def del_gen():
    try:
        for _, v in rcfg("docs/_meta.yml")["generated"].items():
            for i in v["folders"]:
                if path.isdir(i):
                    shutil.rmtree(i)
            for i in v["files"]:
                if path.isfile(i):
                    os.remove(i)
    except TypeError:
        shutil.copy("docs/_meta.bak.yml", "docs/_meta.yml")
        del_gen()


def main(rmv: Dict[Any, Any] = {}, hr=False):
    docs_pdir = DOCS["op"]
    rmv_r = rmv["rules"]
    rmv_mv = rmv["md_vars"]

    rmv_mv_g = rmv_mv["global"]

    del_gen()

    for rip in list(IDF.rglob("*.ymd")):
        out = path.join(docs_pdir, *rip.parts[2:-1], f"{rip.stem}.md")
        GEN["docs"][1].append(out)

        rf = frontmatter.load(rip)
        md = repl(rf.content, rmv_r)

        d = dict(
            rmv_mv_g,
            **rmv_mv.dir(f"local/{rip.stem}", {}),
        )
        for k, v in d.items():
            md = md.replace(f"${{{k}}}", v)

        if title := rf.get("title"):
            if link := rf.get("link"):
                md = """<h1 align="center" style="font-weight: bold">
    <a target="_blank" href="{}">{}</a>
</h1>\n\n{}\n""".format(
                    link, title, md
                )
            else:
                md = """<h1 align="center" style="font-weight: bold">
    {}
</h1>\n\n{}\n""".format(
                    title, md
                )

        with open(inmd(out, GEN["docs"][0]), "w") as f:
            f.write(md)

    for module_name, yt in yield_text(PROJECT):
        _dd = docs_dir(module_name, api=True)
        with open(_dd, "w") as f:
            f.write(yt)
        GEN["pdoc"][1].append(_dd)

    makos = []

    for g in MAKO["gen"]["glob"]:
        for i in list(Path(".").rglob(g)):
            makos.append(str(i))

    for i in MAKO["gen"]["path"]:
        ip = path.join(DOCS["input"], i)
        if path.isfile(ip):
            makos.append(ip)
        else:
            print(f"{ip} not found")

    for ip in makos:
        pip = Path(ip)
        op = path.join(docs_pdir, *pip.parts[2:-1], f"{pip.stem}.md")
        mytemplate = Template(filename=ip)
        tpl_rd = mytemplate.render(
            **{
                "cwd": dn(ip),
            }
        )
        with open(op, "w") as f:
            f.write(tpl_rd)
        GEN["mako"][1].append(op)

    shutil.copy("docs/_meta.yml", "docs/_meta.bak.yml")
    dm = rcfg("docs/_meta.yml")
    for k, v in GEN.items():
        dm["generated"][k] = {}
        for key, i in zip(["folders", "files"], v):
            dm["generated"][k][key] = list(set(i))
    dm["generated"] = dict(dm["generated"])
    wcfg("docs/_meta.yml", dm)

    if not hr:
        base = "dev/raw_docs/docs"

        ndd = {}
        for u in listdir(base):
            for d in listdir(path.join(base, u)):
                ndd[f"{u}.{d}"] = f"docs/{u}/{d}/"

        lk = list(ndd.keys())[-1]
        ndd[f"{lk} (Current)"] = ndd.pop(lk)
        nd = yaml.dump(ndd, default_flow_style=False)
        nd = "\n".join([f"    - {i}" for i in nd.strip().split("\n")][::-1])

        with open("mkdocs.yml", "r") as f:
            mkdocs = f.read()

        info_yml = {}
        for k, (f, kls) in {
            "site_name": [None, ["project_name"]],
            "site_url": ["https://{}", ["site"]],
            "repo_url": ["https://github.com/{}/{}", ["organization", "repo_name"]],
            "site_description": [None, ["long_desc"]],
            "site_author": [None, ["author"]],
            "copyright": ["Copyright &copy; {} {}", ["year", "author"]],
        }.items():
            vd = {i: rmv_mv_g.get(i, None) for i in kls}
            if f is None:
                op = " ".join(vd.values())
            else:
                op = f.format(*vd.values(), **vd)
            info_yml[k] = op
        mkdocs = re.sub(
            RE_MDSE.format(key="info"),
            yaml.dump(info_yml, indent=2, sort_keys=False),
            mkdocs,
            0,
            re.S,
        )

        with open("mkdocs.yml", "w") as f:
            f.write(re.sub(RE_MDSE.format(key="nav docs"), nd, mkdocs, 0, re.S))
        shutil.copy("mkdocs.yml", "mkdocs.bak.yml")

    run("mkdocs build --site-dir dev/site")

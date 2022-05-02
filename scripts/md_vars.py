import base64
from datetime import date
from functools import partial

from . import docs
from .settings import stg
from .utils import ddir

icons = ["issues", "forks", "stars", "contributors", "license", "code"]
langs = ["python", "html", "yaml"]

def b64(name: str):
    with open(f"./docs/assets/images/icons/{name}", "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

YML = stg(None, "dev.yml")
GLOBAL = partial(ddir, ddir(YML, "md_vars/global"))
LICENSE = partial(ddir, ddir(YML, "license"))

PN = GLOBAL("project_name")
ORG = GLOBAL("organization")
USER = GLOBAL("user")

if (copyright := []) == []:
    c = LICENSE("cholder")
    for u, op in c.items():
        for org, projects in op.items():
            for project, v in projects.items():
                copyright.append(
                    f"by [Github Account [{u}](https://github.com/{u}) Owner, {v['year']}] as part of project [{project}](https://github.com/{org}/{v['year']})"
                )
    if len(copyright) > 1:
        copyright[-2] += f", and {copyright[-1]}"
        del copyright[-1]
    cholder = f"""Copyright for portions of project [{PN}](https://github.com/{ORG}/{PN}) are held {', '.join(copyright)}.\n
All other copyright for project [{PN}](https://github.com/{ORG}/{PN}) are held by [Github Account [{USER}](https://github.com/{USER}) Owner, {LICENSE('year')}]."""
else:
    cholder = f"Copyright (c) 2021 Github Account [{PN}](https://github.com/{USER}) Owner"

RULES_MDV = {
    "rules": {
        "del": {},
        "repl": {},
    },
    "md_vars": {
        "global": {
            "year": str(date.today().year),
            "cholder": cholder,
            **{f"{i}_b64": b64(f"{i}.png") for i in icons}
        },
        "local": {},
    }
}

def main(hr=False):
    docs.main(RULES_MDV, hr)
import base64
from datetime import date

from .cfg import rcfg

icons = ["issues", "forks", "stars", "contributors", "license", "code"]
langs = ["python", "html", "yaml"]

OP_CHOLDER_TPL = """by [{cholder}, Github account <a target=_blank
href="https://github.com/{user}">{user}</a> owner, {year}] as part of project
<a target=_blank href="https://github.com/{org}/{project}">{project}</a>"""

M_CHOLDER_TPL = """Copyright for portions of project <a target=_blank
href="https://github.com/{org}/{project}">{project}</a> are held {mc}.

All other copyright for project <a target=_blank
href="https://github.com/{org}/{project}">{project}</a> are held by [Github
Account <a target=_blank href="https://github.com/{user}">{user}</a> Owner, {year}]."""

S_CHOLDER_TPL = """Copyright (c) {year} Github Account <a target=_blank
href="https://github.com/{user}">{user}<a> Owner"""


def b64(name: str):
    with open(f"./docs/assets/images/icons/{name}", "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


YML = rcfg("dev/vars.yml")
VYML = rcfg("version.yml")

LICENSE = YML["license"]
MD_VARS = YML["md_vars"]

GLOBAL = MD_VARS["global"]

PN = GLOBAL["project_name"]
ORG = GLOBAL["organization"]
USER = GLOBAL["user"]

copyright = []

if LICENSE["cholder"]:
    for c, mp in LICENSE["cholder"].items():
        user = mp["user"]
        for org, projects in mp["projects"].items():
            for project, pm in projects.items():
                copyright.append(
                    OP_CHOLDER_TPL.format(
                        cholder=c,
                        org=org,
                        project=project,
                        user=user,
                        year=pm["year"],
                    )
                )
    if len(copyright) > 1:
        copyright[-2] += f", and {copyright[-1]}"
        del copyright[-1]
    cholder = M_CHOLDER_TPL.format(
        mc=", ".join(copyright), org=ORG, project=PN, user=USER, year=LICENSE["year"]
    )
else:
    cholder = S_CHOLDER_TPL.format(user=USER, year=LICENSE["year"])

MD_VARS["global"] = {
    **GLOBAL,
    "year": str(date.today().year),
    "cholder": cholder,
    **{f"{i}_b64": b64(f"{i}.png") for i in icons},
}

RMDV = {"rules": YML["rules"], "md_vars": MD_VARS}

import base64
from datetime import date

from .cfg import rcfg

# Constants
ICONS = ["issues", "forks", "stars", "contributors", "license", "code"]
LANGS = ["python", "html", "yaml"]
OS = ["linux", "win"]

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

# Derived Constants
BYML = rcfg(".github/workflows/build.yml")
VYML = rcfg("version.yml")
YML = rcfg("dev/vars.yml")

JOBS = BYML["jobs"]
VLS = VYML["ls"]
LICENSE = YML["license"]
MD_VARS = YML["md_vars"]

GLOBAL = MD_VARS["global"]

PN = GLOBAL["project_name"]
ORG = GLOBAL["organization"]
USER = GLOBAL["user"]

# Initialize
copyright = []

# Functions
def b64(name: str):
    with open(f"./docs/assets/images/icons/{name}", "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


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


global_append = {
    "year": str(date.today().year),
    "cholder": cholder,
}

for i in OS:
    for j in JOBS[i]["steps"]:
        if j["name"] == "Build":
            global_append[f"build_{i}"] = j["run"]
            pass

for idx, i in enumerate(["user", "dev", "minor", "patch", "pri", "prv"]):
    global_append[f"ver_{i}"] = str(VLS[idx])

for i in ICONS:
    global_append[f"{i}_b64"] = b64(f"{i}.png")


MD_VARS["global"] = {
    **GLOBAL,
    **global_append,
}

RMDV = {"rules": YML["rules"], "md_vars": MD_VARS}

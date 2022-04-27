import base64
from datetime import date

from . import docs

icons = ["issues", "forks", "stars", "contributors", "license", "code"]
langs = ["python", "html", "yaml"]

def b64(name: str):
    with open(f"./docs/assets/images/icons/{name}", "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

RULES_MDV = {
    "rules": {
        "del": {},
        "repl": {},
    },
    "md_vars": {
        "global": {
            "year": str(date.today().year),
            **{f"{i}_b64": b64(f"{i}.png") for i in icons}
        },
        "local": {},
    }
}

def main():
    docs.main(RULES_MDV)
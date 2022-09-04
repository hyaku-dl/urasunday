import re
from os import path
from typing import Any

import inquirer

from . import scripts
from .cfg import rcfg, wcfg
from .md_vars import RMDV, VYML
from .schema import Config
from .utils import run

# Constants
VERSIONS_NAME = [
    "User",
    "Dev",
    "Minor",
    "Patch",
    "Pre-release identifier",
    "Pre-release version",
]
PR = ["alpha", "beta", "rc"]
DE_PUSH_MSG = "For info, check `docs/latest commit.md` or this commit's comments"
PUSH_CMD = 'git commit -am "{}"'

# Derived Constants
GLOBAL = RMDV["md_vars"]["global"]
VLS_STR_RE = re.compile(r"^(((0|[1-9][0-9]*) ){4}([0-2] (0|[1-9][0-9]*)|3 0))$")
VLS = VYML["ls"]
META_YML = rcfg(
    path.join("dev/constants/version", *[str(_) for _ in VLS[0:2]], "_meta.yml")
)


def cc():
    for k, v in META_YML["cp"].items():
        wcfg(
            f'{v["dir"]}.{v.get("ext", "mp")}',
            rcfg(
                path.join(
                    "dev/constants/version", *[str(_) for _ in VLS[0:2]], f"{k}.yml"
                )
            ),
        )

    cf_tpl = rcfg(
        path.join("dev/constants/version", *[str(_) for _ in VLS[0:2]], "config.yml")
    )
    Config(cf_tpl["version"])(cf_tpl["config"])

    init_file = "ura/src/__init__.py"
    with open(init_file, "r") as f:
        op = f.read()
    with open(init_file, "w") as f:
        f.write(re.sub(r'(cholder = """)(.*?)(?="""|$)', f'$1{GLOBAL["cholder"]}', op))


def docs():
    from .docs import main
    from .md_vars import RMDV

    cc()
    scripts.main()

    main(RMDV)


def fmt():
    run("bash dev/scripts/sh/source.sh fmt")


def push(v: list[int] = None):
    cc()
    msg = inquirer.text(message="Enter commit message", default="")
    run("git add .")
    if msg == "":
        msg = DE_PUSH_MSG
    if v:
        msg = "\n".join(
            [
                msg,
                f"Release notes: https://{GLOBAL['site']}/changelog#{'-'.join([str(i) for i in v])} or `docs/latest release notes.md`",
            ]
        )
    fmt()
    run(PUSH_CMD.format(msg))
    run("git push")


def vls_str(vls: list[str]) -> list[str]:
    pr = ""
    if vls[4] < 3:
        pr = f"-{PR[vls[4]]}.{vls[5]}"
    return [
        ".".join([str(i) for i in vls[0:4]]) + pr,
        ".".join([str(i) for i in [*vls[0:2], 3 ** vls[2] * 2 ** vls[3]]]) + pr,
    ]


def dcomp(x: int) -> list[int]:
    """Given a number x, return a list of times a prime factor of x occured.

    Args:
        x (int): Number to get the prime factors of.

    Returns:
        list[int]: List of times a prime factor of x occured.
    """
    primes = [3, 2]
    factors = [0 for _ in primes]
    while x != 1:
        for idx, i in enumerate(primes):
            if x % i == 0:
                factors[idx] += 1
                x = x / i
                break
            else:
                pass
    return factors


def py_var_sub(file: str, kv: dict[str, Any]) -> None:
    with open(file, "r") as f:
        op = f.read()
    for k, v in kv.items():
        if isinstance(v, str):
            if "'" in v:
                v = f'"{v}"'
            else:
                v = f"'{v}'"
        op = re.sub(rf"{k}.+", f"{k} = {v}", op, count=1)
    with open(file, "w") as f:
        f.write(op)


def _set_ver(vls: list[int]) -> None:
    """Set version, and write to file.

    Args:
        vls (list[int]): Version list.
    """
    op_ls = [vls, *vls_str(vls)]
    wcfg("version.yml", {k: v for k, v in zip(["ls", "str", "sv"], op_ls)})
    py_var_sub(
        "ura/src/__init__.py",
        {k: v for k, v in zip(["vls", "__version__", "hver"], op_ls)},
    )


def vfn(answers: list[Any], current: str) -> bool:
    x, y = VLS_STR_RE.match(current).span()
    vls = current[x:y].strip().split(" ")
    if len(vls) == 5:
        _set_ver([int(i) for i in vls])
        return True

    raise Exception("Invalid version digits")


def vlir(idx: int, vls: list[int]) -> list[int]:
    """Version Lower than Index will be Reset

    Args:
        idx (int): Index to compare to.
        vls (list[int], optional): Version list.

    Returns:
        list[int]: Modified version list.
    """

    for i in range(idx + 1, len(vls)):
        if i == 4:
            vls[i] = 3
        else:
            vls[i] = 0
    return vls


def _bump(idx: int) -> list[int]:
    """_summary_

    Args:
        idx (int): Index to bump.

    Returns:
        list[int]: Modified version list.
    """

    _vls = list(VLS)
    if idx == 4:
        if _vls[idx] == 3:
            _vls[3] += 1
            _vls[4] = _vls[5] = 0
        else:
            _vls = vlir(idx, _vls)
            _vls[idx] += 1
    else:
        _vls = vlir(idx, _vls)
        _vls[idx] += 1
    return _vls


def bump():
    while True:
        choices = []
        for idx, k in enumerate(VERSIONS_NAME):
            choices.append([f"{k.ljust(23)}(bump to {vls_str(_bump(idx))[0]})", idx])
        idx = inquirer.list_input(
            message=f"What version do you want to bump? (Current version: {vls_str(VLS)[0]})",
            choices=choices,
        )
        _vls = _bump(idx)
        print(
            f"    This will bump the version from {vls_str(VLS)[0]} to {vls_str(_vls)[0]} ({VERSIONS_NAME[idx]} bump). "
        )
        match inquirer.list_input(
            message="Are you sure?",
            choices=[
                ["Yes", "y"],
                ["No", "n"],
                ["Cancel", "c"],
            ],
        ):
            case "y":
                _set_ver(_vls)
                scripts.main()
                push(_vls)
                return
            case "n":
                continue
            case "c":
                break
            case _:
                pass


def main(choice: str = None):
    match choice or inquirer.list_input(
        message="What action do you want to take",
        choices=[
            ["Copy constants", "cc"],
            ["Generate documentation", "docs"],
            ["Push to github", "gh"],
            ["Bump a version", "bump"],
            ["Generate scripts", "gs"],
            ["Set the version manually", "set_ver"],
        ],
    ):
        case "cc":
            cc()
        case "docs":
            pp = inquirer.confirm("Do you want to push this to github?", default=False)
            docs()
            if pp:
                push()
        case "gh":
            docs()
            push()
        case "gs":
            scripts.main()
        case "bump":
            docs()
            bump()
        case "set_ver":
            inquirer.text(
                message="Enter version digits seperated by spaces", validate=vfn
            )
        case _:
            run(f"bash dev/scripts/sh/source.sh {choice}")

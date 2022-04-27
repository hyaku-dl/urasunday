import re
import shlex
import sys
from os import path
from subprocess import call

VERSIONS_NAME = {
    "user": "User",
    "dev": "Dev",
    "minor": "Minor",
    "patch": "Patch",
    "pri": "Pre-release identifier",
    "prv": "Pre-release version",
}
VERSIONS = ["user", "dev", "minor", "patch", "pri", "prv"]

PR = ["alpha", "beta", "rc"]

def format():
    run("isort .")

def cp():
    for k, v in META_YML["cp"].items():
        with open(
            path.join("constants", *[str(_) for _ in VLS[0:2]], f'{k}.yml'),
            "r"
        ) as f:
            fc = yaml.safe_load(f.read())
        if v.get("mp", True):
            with open(f'{v["dir"]}.mp', "wb") as f:
                f.write(msgpack.packb(fc, use_bin_type=True))
        else:
            with open(f'{v["dir"]}.yml', "w") as f:
                yaml.dump(fc, f, indent=4)

    cf_tpl = stg(
        None,
        path.join("constants", *[str(_) for _ in VLS[0:2]],
        "config.yml")
    )
    config(cf_tpl["version"])(cf_tpl["config"])

def run(s: str):
    call(shlex.split(s))

def push(v: list[int]=None):
    msg = inquirer.text(message="Enter your username", default="")
    format()
    run("git add .")
    if msg != "":
        msg = f"{msg},"
    if v:
        run(f"git commit -am '{msg}https://hyk.fr.to/changelog#v{'-'.join(v)}'")
    else:
        run(f"git commit -am '{msg or 'push'}'")
    run("git push")

def reset(idx: int):
    _vls = list(VLS)
    for i in range(idx + 1, len(VLS)):
        _vls[i] = 0
    return _vls

def rv(vls: list[str]):
    pr = ""
    if vls[4]:
        pr = f'-{PR[vls[4] - 1]}.{vls[5]}'
    return ".".join([str(i) for i in vls[0:4]]) + pr

def _bump(v: str):
    idx = VERSIONS.index(v)
    _vls = list(VLS)
    match v:
        case "pri":
            match _vls[idx]:
                case 0:
                    _vls[3] += 1
                    _vls[4] = _vls[4] = 1
                case 3:
                    _vls[3] = _vls[4] = 0
                case _:
                    _vls = reset(idx, _vls)
                    _vls[idx] += 1
        case _:
            _vls = reset(idx, _vls)
            _vls[idx] += 1
    return _vls

def bump():
    while True:
        choices = []
        for k, v in VERSIONS_NAME.items():
            choices.append([f'{k.ljust(23)}(bump to {rv(_bump(k, VLS))})', k])
        v = inquirer.list_input(
            message=f"What version do you want to bump? (Current version: {rv(VLS)})",
            choices=choices,
        )
        _vls = _bump(v, VLS)
        print(
            f"    This will bump the version from {rv(VLS)} to {rv(_vls)} ({VERSIONS_NAME[v]} bump). "
        )
        match inquirer.list_input(
            message="Are you sure?",
            choices=[
                ["Yes", "y"],
                ["No", "n"],
                ["Cancel", "c"],
            ]
        ):
            case "y":
                with open("version", "wb") as f:
                    f.write(msgpack.packb(_vls, use_bin_type=True))
                with open("ura/__init__.py", "r") as f:
                    init = f.read()
                with open("ura/__init__.py", "w") as f:
                    init = re.sub(r"__version__.+", f"__version__ = {v}", init)
                    init = re.sub(r"vls.+", f"vls = {_vls}", init)
                    f.write(re.sub(r"__version__.+", f"__version__ = {v}", init))
                push(_vls)
                return
            case "n":
                continue
            case "c":
                break
            case _:
                pass

def vfn(answers, current):
    global vls
    x, y = re.match(r"((\d+\s*){6})", current).span()
    vls = current[x:y].strip().split(" ")
    if len(vls) == 6:
        vls = [int(i) for i in vls]
        return True

    raise Exception("Invalid version digits")

def set_ver():
    inquirer.text(
        message="Enter version digits seperated by spaces",
        validate = vfn
    )

    with open("version", "wb") as f:
        f.write(msgpack.packb(vls, use_bin_type=True))

    with open("ura/__init__.py", "r") as f:
        init = f.read()

    with open("ura/__init__.py", "w") as f:
        init = re.sub(r"vls.+", f"vls = {vls}", init)
        f.write(re.sub(r"__version__.+", f"__version__ = '{rv(vls)}'", init))

def main():
    match inquirer.list_input(
        message="What action do you want to take",
        choices=[
            ["Copy constants to project folder", "cp"],
            ["Format code", "f"],
            ["Generate documentation", "docs"],
            ["Push to github", "gh"],
            ["Bump a version", "bump"],
            ["Set the version manually", "set_ver"]
        ]
    ):
        case "cp":
            cp()
        case "f":
            format()
        case "docs":
            cp()
            from scripts import md_vars
            md_vars.main()
            if inquirer.confirm(
                "Do you want to push this to github?",
                default=False
            ):
                push()
        case "gh":
            cp()
            push()
        case "bump":
            bump()
        case "set_ver":
            set_ver()
        case _:
            pass

if __name__ == "__main__":
    if ((len(sys.argv) >= 2) and (sys.argv[1] == "req")):
        run(f'pip install --require-virtualenv pyyaml')
        import yaml
        with open('dev.yml', 'r') as f:
            y = yaml.safe_load(f)
        ls = []
        for C in y["env"]["dev"]["req"]:
            ls.append(f'-r {y["requirements"][C]}')
        run(f'pip install --require-virtualenv {" ".join(ls)}')
    else:
        import inquirer
        import msgpack
        import yaml

        from scripts.schema import config
        from scripts.settings import stg

        with open("version", "rb") as f:
            VLS = msgpack.unpackb(f.read(), raw=False, use_list=False)

        META_YML = stg(
            None,
            path.join("constants", *[str(_) for _ in VLS[0:2]], "_meta.yml")
        )

        main()
import locale
import os
import sys
from os import get_terminal_size, makedirs, path
from os.path import abspath as ap
from os.path import dirname as dn

import inquirer
import msgpack
import yaml

try:
    TW = get_terminal_size().columns
except OSError as e:
    TW = None

CFLOP = ""
"""
```mermaid
flowchart LR
    A([Config]) --> B[Grab CFLOP]
    B --> C{Last item}
        C --> |false| D{File exists?}
            D --> |true| E([Read config file])
            D --> |false| C
        C --> |true| F{OS?}
            F --> |Windows| G[Initialize config file<br>at first lookup path] --> E
            F --> |*nix| H{.AppImage?}
                H --> |true| I[Initialize config file<br>at second lookup path] --> E
                H --> |false| G
```
"""


def init(idx: int) -> None:
    global CFG_PATH
    with open(path.join(dn(ap(__file__)), "cf_tpl.mp"), "rb") as f:
        cm = msgpack.unpackb(f.read(), raw=False, use_list=True)

    if sys.platform == "win32":
        ddir = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop", "Manga")
    else:
        ddir = os.path.join(os.path.expanduser("~"), "Manga")

    if TW:
        validate = False
        while not validate:
            if inquirer.list_input(
                message="Choose the path to download the chapter to",
                choices=[
                    [ddir, False],
                    ["Input it myself", True],
                ],
            ):
                pd = input("Input the path to download the chapter to: ")
                if not path.isdir(pd):
                    if inquirer.confirm(
                        "The path does not exist. Do you want to make it?",
                        default=False,
                    ):
                        makedirs(pd)
                        validate = True
                ddir = pd
            else:
                validate = True

    cm["download_dir"] = ddir
    CFG_PATH = CFLOP[idx]
    with open(CFLOP[idx], "w") as f:
        f.write(yaml.dump(cm, indent=2))


if os.name != "posix":
    import ctypes

    POSIX = 0

    CFLOP = [
        rf"{os.getcwd()}\ura.yml",
        rf"{os.getenv('USERPROFILE')}\AppData\Roaming\ura\config.yml",
    ]
    LOCALE = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()][
        :2
    ]
else:
    POSIX = 1
    CFLOP = [f"{os.getcwd()}/ura.yml", "~/.config/ura/config.yml", "~/.ura"]
    if xch := os.getenv("XDG_CONFIG_HOME"):
        CFLOP.insert(1, f"{xch}/ura/config.yml")
    LOCALE = locale.getdefaultlocale()[0][:2]


CFG_PATH = None
for i in CFLOP:
    if os.path.exists(str(i)):
        CFG_PATH = i
        break

if CFG_PATH is None:
    if POSIX:
        try:
            from . import appimage
        except ImportError:
            from __init__ import appimage

        if appimage:
            init(1)
        else:
            init(0)
    else:
        init(0)

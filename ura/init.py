import os
import random
import sys
from os import makedirs, path
from os.path import abspath as ap
from os.path import dirname as dn

import inquirer

from .globals import CFLOP, POSIX, TW
from .settings import stg, wr_stg
from .style import S, ct, pp

title = S.p1(S.t1("comic-dl/urasunday"))

tww = []

if TW < 40:
    tww = [
        S.t_error("Your terminal width is well below than"),
        S.t_error("the bare minimum"),
        S.t_error(f"({TW} instead of 40 and above)"),
        S.t_error(f"Consider resizing\n")
    ]
else:
    if TW < 55:
        tww = [
                S.t_warning("Your terminal width is below than"),
                S.t_warning(f"recommended ({TW} instead of 55 and above)\n")
            ]

wcd = stg(None, "ura/hc.yml")

pp(
    ct.group(
        title,
        S.t1("Your basic urasunday scraper."),
        S.t1("\nConsider donating to the project: https://hyaku.download/donate\n"),
        S.t0("{}\n".format(random.choice(wcd["random"]))),
        *tww,
    )
)

def init(idx: int) -> None:
    cm = stg(None, path.join(dn(ap(__file__)), "cf_tpl.mp"))

    if sys.platform == "win32":
        ddir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'Manga')
    else:
        ddir = os.path.join(os.path.expanduser('~'), "Manga")

    validate = False
    while not validate:
        if inquirer.list_input(
            message="Choose the path to download the chapter to",
            choices=[
                [ddir, False],
                ["Input it myself", True],
            ]
        ):
            pd = input("Input the path to download the chapter to: ")
            if not path.isdir(pd):
                if inquirer.confirm("The path does not exist. Do you want to make it?", default=False):
                    makedirs(pd)
                    validate = True
        else:
            validate = True
    cm["download_dir"] = ddir
    wr_stg(None, cm, CFLOP[idx])

config_path = None
for i in CFLOP:
    if os.path.exists(str(i)):
        config_path = i
        break

if config_path is None:
    if POSIX:
        from . import appimage
        if appimage:
            init(1)
        else:
            init(0)
    else:
        init(0)
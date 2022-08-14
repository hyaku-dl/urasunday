import os
import random
import sys
from os import makedirs, path
from os.path import abspath as ap
from os.path import dirname as dn

import inquirer

from . import globals
from .cfg import rcfg, wcfg
from .globals import CFLOP, POSIX, TW
from .style import S, ct, pp

if TW:
    title = S.p1(S.t1("comic-dl/urasunday"))

    tww = []

    if TW < 40:
        tww = [
            S.t_error("Your terminal width is well below than"),
            S.t_error("the bare minimum"),
            S.t_error(f"({TW} instead of 40 and above)"),
            S.t_error("Consider resizing\n"),
        ]
    else:
        if TW < 55:
            tww = [
                S.t_warning("Your terminal width is below than"),
                S.t_warning(f"recommended ({TW} instead of 55 and above)\n"),
            ]

    wcd = rcfg(path.join(dn(ap(__file__)), "hc.yml"))

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
    cm = rcfg(path.join(dn(ap(__file__)), "cf_tpl.mp"))

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
    globals.CFG_PATH = CFLOP[idx]
    wcfg(CFLOP[idx], cm)


if globals.CFG_PATH is None:
    if POSIX:
        from . import appimage

        if appimage:
            init(1)
        else:
            init(0)
    else:
        init(0)

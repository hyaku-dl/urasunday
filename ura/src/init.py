import random
from os import path
from os.path import abspath as ap
from os.path import dirname as dn

try:
    from .cfg import rcfg
    from .globals import TW
    from .style import S, ct, pp
except ImportError:
    from cfg import rcfg
    from globals import TW
    from style import S, ct, pp

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

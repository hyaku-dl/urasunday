import builtins
import inspect
import warnings
from functools import partial
from textwrap import wrap
from typing import Any, Callable, List

import click
from tabulate import tabulate

warnings.filterwarnings("ignore")

try:
    from .cfg import rcfg
    from .download import Downloader
    from .globals import TW
    from .style import S, pp
    from .utils import dnrp
except ImportError:
    from cfg import rcfg
    from download import Downloader
    from globals import TW
    from style import S, pp
    from utils import dnrp

# Constants
LVLS = [
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
    "NOTSET",
]

# Derived Constants
CMD = rcfg(f"{dnrp(__file__)}/cmd.mp")


class cao:
    """Returns wrappers for a click command evaluated from the given arguments."""

    # def __init__(
    #     self, group, cmd: str
    # ) -> List[Callable[[Callable[[Any], Any]], Callable[[Any], Any]]]:

    #     """
    #     Args:
    #     - group (`click.group`): Command group of the command to be under.
    #     - cmd (`str`): Name of the command.

    #     Returns:
    #     `List[Callable[[Callable[[Any], Any]], Callable[[Any], Any]]]`: The wrappers.
    #     """

    #     self.group = group
    #     self.cmd = cmd = CMD.dir(f"cmd/{cmd}")
    #     self.arguments = cmd["arguments"]

    def c(
        self, f: Callable[[Any], Any]
    ) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """The command wrapper.

        Args:
        - f (`Callable[[Any], Any]`): The command function to be decorated.
        Returns:
        `Callable[[Callable[[Any], Any]], Callable[[Any], Any]]`
        """

        help = []
        if self.arguments:
            for k, v in self.arguments.items():
                self.arguments[k]["help"] = [
                    *v["help"],
                    *[None for _ in range(3 - len(v["help"]))],
                ]
            for k, v in self.arguments.items():
                vh = v["help"]
                if len(vh) < 3:
                    vh = [*vh, *[None for _ in range(3 - len(vh))]]
                t, h, e = vh
                e = "\nEx.: {e}" if e else ""
                help.append([f"<{k}>", t, f"{h}{e}"])
        s, h = self.cmd["help"]
        return self.group.command(
            *(self.cmd["args"] or []),
            **dict(
                {
                    "context_settings": {"help_option_names": ["-h", "--help"]},
                    "short_help": s,
                    "help": f"\b\n{h}\n{tabulate(help, tablefmt='plain')}",
                },
                **(self.cmd["kwargs"] or {}),
            ),
        )(f)

    def a(
        self, f: Callable[[Any], Any]
    ) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """The arguments wrapper.

        Args:
        - f (`Callable[[Any], Any]`): The command function to be decorated.
        Returns:
        `Callable[[Callable[[Any], Any]], Callable[[Any], Any]]`
        """
        args = {}
        kwargs = {}
        if self.arguments:
            for k, v in self.arguments.items():
                kw = {"metavar": f"<{k}>"}
                args[k] = [k, *(v["args"] or [])]
                kwargs[k] = dict(kw, **(v["kwargs"] or {}))
            for i in list(args.keys()):
                f = click.argument(*args[i], **kwargs[i])(f)
        return f

    def o(
        self, f: Callable[[Any], Any]
    ) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """The options wrapper.
        My God in heaven, I'm agnostic, but please save me from all evil. Amen.

        Args:
        - f (`Callable[[Any], Any]`): The command function to be decorated.
        Returns:
        `Callable[[Callable[[Any], Any]], Callable[[Any], Any]]`
        """
        if opts := self.cmd["options"]:
            n = 0
            on = 0
            args = {}
            kwargs = {}

            for k, v in opts.items():
                l = len(v["help"][0] or "")
                n = l if l > n else n

                ol = len(f'-{k}, --{v["args"][0]}')
                on = ol if ol > on else on

                opts[k]["help"] = [
                    *v["help"],
                    *[None for _ in range(3 - len(v["help"]))],
                ]
            n += 2
            on += 4
            al = TW - (n + on)
            for k, v in opts.items():
                a = v["args"] or []
                kw = v["kwargs"] or {}
                a[0] = f"--{a[0]}"
                a.insert(0, f"-{k}")
                kt = kw.get("type", None)
                vh = v["help"]
                if len(vh) < 3:
                    vh = [*vh, *[None for _ in range(3 - len(vh))]]
                t, h, e = vh
                t = t or ""
                if h:
                    h = "\n".join(
                        wrap(
                            h.replace("\n", "\n" + " " * n),
                            width=al,
                            subsequent_indent=" " * n,
                            replace_whitespace=False,
                        )
                    )
                else:
                    h = ""
                if e:
                    els = []
                    for i, j in enumerate(e.split("\n")):
                        els.append(
                            "{}{}{}".format(
                                " " * (n + (11 if i else 6)),
                                "Ex.: " if not i else "",
                                j,
                            )
                        )
                    e = "\n" + "\n".join(els)
                else:
                    e = ""
                kw["help"] = f'\b\n{t}{" "*(n - len(t))}{h}{e}'
                if isinstance(kt, dict):
                    ktk, ktv = list(kt.items())[0]
                    kta, ktkw = [i[1] for i in ktv.items()]
                    kw["type"] = getattr(click, ktk)(*kta, **ktkw if ktkw else {})
                elif kt:
                    kw["type"] = getattr(builtins, kt)
                args[k] = a
                kwargs[k] = kw
            for i in list(args.keys()):
                f = click.option(*args[i], **kwargs[i])(f)
        return f

    def __new__(
        self, group, cmd: str
    ) -> List[Callable[[Callable[[Any], Any]], Callable[[Any], Any]]]:

        """
        Args:
        - group (`click.group`): Command group of the command to be under.
        - cmd (`str`): Name of the command.

        Returns:
        `List[Callable[[Callable[[Any], Any]], Callable[[Any], Any]]]`: The wrappers.
        """

        self.group = group
        self.cmd = cmd = CMD.dir(f"cmd/{cmd}")
        self.arguments = cmd["arguments"]
        return partial(self.c, self), partial(self.a, self), partial(self.o, self)


def command(
    group,
) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
    """Wrapper for click commands.

    Args:
    - group (`click.group`): Command group of the command to be under.

    Returns:
    - `Callable[[Callable[[Any], Any]], Callable[[Any], Any]]`
    """

    def inner(f: Callable[[Any], Any]):
        m = inspect.getouterframes(inspect.currentframe())[1][4][0]
        for m in cao(group, m[4 : m.index("(")]):
            f = m(f)
        return f

    return inner


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """Main command group."""


@command(cli)
def dl(url: str, **kwargs: dict[str, Any]):
    """Download chapter from https://urasunday.com

    Args:
    - url (`str`): URL of the chapter to download.
    """
    Downloader(**kwargs).dlch(url)


@command(cli)
def version():
    """Print version of the program."""
    from __init__ import __version__

    pp(S.p1(__version__))

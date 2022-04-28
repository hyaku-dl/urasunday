import builtins
import inspect
import logging
from typing import Any, Callable, List

import click
from rich.logging import RichHandler
from tabulate import tabulate

from . import init  # type: ignore
from . import globals
from .download import Downloader
from .settings import stg
from .style import S, pp
from .utils import dd, de, dnrp

LVLS = [
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
    "NOTSET",
]

def fn_log(lvl: int):
    if lvl == 1:
        l = "NOTSET"
    else:
        l = LVLS[lvl - 2]

    logging.basicConfig(
        level=l,
        format="%(message)s",
        datefmt="[%H:%M:%S.%f]",
        handlers=[RichHandler(
            omit_repeated_times=False,
            markup=True,
            rich_tracebacks=True
        )]
    )

    op = logging.getLogger("rich")
    if lvl == 1:
        logging.disable()
    globals.log = op

def cao(
    group: click.group, cmd: str
) -> List[Callable[[Callable[[Any], Any]], Callable[[Any], Any]]]:
    """
    Retruns wrappers for a click command evaluated from the given arguments.

    Args:
        group (click.group): Command group of the command to be under.
        cmd (str): Name of the command.

    Returns:
        List[Callable[[Callable[[Any], Any]], Callable[[Any], Any]]]: The wrappers.
    """
    cmd = stg(f"cmd/{cmd}", f"{dnrp(__file__)}/cmd.mp")
    arguments = cmd["arguments"]

    def c(
        f: Callable[[Any], Any]
    ) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """
        The command wrapper.
        Args:
            f (Callable[[Any], Any]): The command function to be decorated.
        Returns:
            Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
        """

        help = []
        if arguments:
            for k, v in arguments.items():
                arguments[k]["help"] = [
                    *v["help"],
                    *[None for _ in range(3 - len(v["help"]))]
                ]
            for k, v in arguments.items():
                t, h, e = v["help"]
                e = '\nEx.: {e}' if e else ""
                help.append([f"<{k}>", t, f'{h}{e}'])
        s, h = cmd["help"]
        return group.command(
            *de(cmd["args"], []),
            **dd(
                {
                    "context_settings": {'help_option_names': ['-h', '--help']},
                    "short_help": s,
                    "help": f"\b\n{h}\n{tabulate(help, tablefmt='plain')}"
                },
                cmd["kwargs"]
            )
        )(f)

    def a(
        f: Callable[[Any], Any]
    ) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """
        The arguments wrapper.
        Args:
            f (Callable[[Any], Any]): The command function to be decorated.
        Returns:
            Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
        """
        args = {}
        kwargs = {}
        if arguments:
            for k, v in arguments.items():
                kw = {"metavar": f"<{k}>"}
                args[k] = [k, *de(v["args"], [])]
                kwargs[k] = dd(kw, v["kwargs"])
            for i in list(args.keys()):
                f = click.argument(*args[i], **kwargs[i])(f)
        return f

    def o(
        f: Callable[[Any], Any]
    ) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """
        The options wrapper.
        My God in heaven, I'm agnostic, but please save me from all evil. Amen.

        Args:
            f (Callable[[Any], Any]): The command function to be decorated.
        Returns:
            Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
        """
        if opts:= cmd["options"]:
            n = 0
            args = {}
            kwargs = {}
            for k, v in opts.items():
                l = len(v["help"][0] or "")
                n = l if l > n else n
                opts[k]["help"] = [
                    *v["help"],
                    *[None for _ in range(3 - len(v["help"]))]
                ]
            for k, v in opts.items():
                a = de(v["args"], [])
                kw = de(v["kwargs"], {})
                a[0] = f"--{a[0]}"
                a.insert(0, f"-{k}")
                kt = kw.get("type", None)
                t, h, e = v["help"]
                t = t or ""
                if h:
                    hls = []
                    for i, j in enumerate(h.split("\n")):
                        if i:
                            spn = 0
                        else:
                            spn = len(j)
                        hls.append(f'{" " * ((n + 3)-spn)}{j}')
                    h = "\n".join(hls)
                else:
                    h = ""
                if e:
                    els = []
                    for i, j in enumerate(e.split("\n")):
                        els.append('{}{}{}'.format(
                                ' ' * (n + (11 if i else 6)),
                                "Ex.: " if not i else "",
                                j
                            )
                        )
                    e = "\n" + "\n".join(els)
                else:
                    e = ""
                kw["help"] = f'\b\n{t}{" "*((n + 3) - len(t))}{h}{e}'
                if isinstance(kt, dict):
                    ktk, ktv = list(kt.items())[0]
                    kta, ktkw = [i[1] for i in ktv.items()]
                    kw["type"] = getattr(
                        click,
                        ktk
                    )(
                        *kta,
                        **ktkw if ktkw else {}
                    )
                elif kt:
                    kw["type"] = getattr(builtins, kt)
                args[k] = a
                kwargs[k] = kw
            for i in list(args.keys()):
                f = click.option(*args[i], **kwargs[i])(f)
        return f

    return c, a, o

def command(
    group: click.group
) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
    """
    Wrapper for click commands.

    Args:
        group (click.group): Command group of the command to be under.

    Returns:
        Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
    """

    def inner(f: Callable[[Any], Any]):
        m = inspect.getouterframes(inspect.currentframe())[1][4][0]
        for m in cao(group, m[4:m.index("(")]):
            f = m(f)
        return f
    return inner

@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """Main command group."""

@command(cli)
def dl(url: str, **kwargs: dict[str, Any]):
    Downloader(**kwargs).dlch(url)

@command(cli)
def version():
    from . import __version__
    pp(S.p1(__version__))
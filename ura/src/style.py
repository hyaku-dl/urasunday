import itertools
from functools import partial
from typing import Any

import rich
from rich import print
from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text

COLORS = {
    "h": [
        "#f2f774",
        "#ff7b42",
        "#e83140"
    ],
    "s": [
        "#F3F78D",
        "#FF8D5C",
        "#E84855"
    ]
}

COLORS_TYPE = {
    "p": {
        "n": [
            "#E68AFF",
            "#9D7DFF",
        ],
        "named": {}
    },
    "t": {
        "n": [
            "#FFF273",
            "#C1ADFF",
            "#FF96C1",
        ],
        "named": {
            "warning": "#FFBA49",
            "error": "#FF9522",
            "critical": "#FA1928",
        }
    },
}

STYLE_TYPE = {
    "p": Panel,
    "t": Text,
}

STYLE_ALL = {
    "all": {
        "padding": [
            0,
            5
        ]
    },
    "table": {
        "box": "ROUNDED",
        "row_styles": [
            "none",
            "dim"
        ],
        "show_lines": True,
        "title_justify": "center",
        "columns": [
            {
                "header_style": "h0",
                "style": "h0",
            },
            {
                "header_style": "h1",
                "style": "h1",
            },
            {
                "header_style": "h2",
                "style": "h2",
            },
        ]
    }
}

class S:
    pass

class C:
    pass

for k, v in STYLE_TYPE.items():
    for idx, i in enumerate(COLORS_TYPE[k]["n"]):
        setattr(S, f"{k}{idx}", partial(v, style=Style(color=i)))
    for vk, vv in COLORS_TYPE[k]["named"].items():
        setattr(S, f"{k}_{vk}", partial(v, style=Style(color=vv)))

for k, v in COLORS.items():
    for idx, i in enumerate(v):
        setattr(C, f"{k}{idx}", i)

def pp(t: Any):
    print(Align.center(t))

class ct:
    def group(*ls: list[Any]) -> Group:
        op = []
        for i in ls:
            op.append(Align.center(i))
        return Group(*op)

    def table(cols: list[str], rows: list[list[str]]):
        stb = STYLE_ALL["table"]
        box = getattr(rich.box, stb.pop("box"))

        new_cols = []
        for title, col in zip(cols, itertools.cycle(stb.pop("columns"))):
            attr = {}
            for i in ["header_style", "style"]:
                attr[i] = getattr(C, col[i])
            new_cols.append(Column(title, **attr, justify="center"))

        t = Table(*new_cols, **stb, **STYLE_ALL["all"], box=box)
        for i in rows:
            t.add_row(*[str(i) for i in i])

        pp(t)
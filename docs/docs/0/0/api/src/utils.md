# Module ura.src.utils

## Functions

`dnrp(file: str, n: int = 1) ‑> str`
:   Get the directory component of a pathname by n times recursively then return it.

```
Args:
    file (str): File to get the directory of.
    n (int, optional): Number of times to get up the directory???? Defaults to 1.

Returns:
    op (str): The directory component got recursively by n times from the given pathname
```

`dpop(d: dict[typing.Any, typing.Any], pop: list[int | tuple[str | int | tuple] | str], de: Any = None) ‑> Any`
:   Iterate through the preferred order of precedence (`pop`) and see if
the value exists in the dictionary. If it does, return it. If not, return
`de`.

```
Args:
    d (Dict[Any, Any]): Dictionary to retrieve the value from.
    pop (list[int | tuple[str | int | tuple] | str]): List of keys to
        iterate through.
    de (Any, optional): Default object to be returned. Defaults to None.

Returns:
    Any: Retrieved value.
```

`dt(dt: str, format: str) ‑> str`
:   Remove timezone from datetime and format it to ISO 8601 format.

```
Args:
    dt (str): Unformatted datetime string to be formatted to ISO 8601 format
    format (str): The initial format of the datetime string

Returns:
    str: Formatted datetime string
```

`dt_ts(ts: str) ‑> str`
:   Convert the given unix timestamp to ISO 8601 format.

```
Args:
    ts (str): unix timestamp to be converted to ISO 8601 format

Returns:
    str: Formatted datetime string
```

`inmd(p: str, ls: list[str] = None)`
:   "If Not `path.isdir`, Make Directories"

```
Args:
    p (str): [description]
```

`ivnd(var: Any, de: Any) ‑> Any`
:   If Var is None, return Default else var.

```
Args:
    var (Any): Variable to check if it is None.
    de (Any): Default value to return if var is None.

Returns:
    Any: var if var is not None else de.
```

`le(expr: str) ‑> Any`
:

`repl(s: str, repl_dict: dict[str, list[str]]) ‑> str`
:

`run(s: str)`
:

`sanitize_text(s: str)`
:

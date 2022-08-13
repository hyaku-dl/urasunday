Module ura.src.utils
====================

Functions
---------

    
`dd(default: dict[typing.Any, typing.Any], d: dict[typing.Any, typing.Any] | None) ‑> dict[typing.Any, typing.Any]`
:   Defaults dictionary. Overwrite the items in the default dict with the
    items in the d dict.
    
    Args:
        default (Dict[Any, Any]): The dict to rewrite the items to.
        d (Union[Dict[Any, Any], None]): The dict to rewrite the items from.
    
    Returns:
        dict[Any, Any]

    
`ddir(d: dict[typing.Any, typing.Any], dir: str, de: Any = {}) ‑> Any`
:   Retrieve dictionary value using recursive indexing with a string.
    ex.:
        `ddir({"data": {"attr": {"ch": 1}}}, "data/attr/ch")`
        will return `1`
    
    
    Args:
        dict (dict): Dictionary to retrieve the value from.
        dir (str): Directory of the value to be retrieved.
    
    Returns:
        op (Any): Retrieved value.

    
`de(a: Any, d: Any) ‑> Any`
:   Defaults. Return a if a is True, else returns d.
    
    Args:
        a (Any): Object to be tested, will be returned if evaluates to True.
        d (Any): Default object to be returned if `a` evaluates to False.
    
    Returns:
        Any

    
`dnrp(file: str, n: int = 1) ‑> str`
:   Get the directory component of a pathname by n times recursively then return it.
    
    Args:
        file (str): File to get the directory of.
        n (int, optional): Number of times to get up the directory???? Defaults to 1.
    
    Returns:
        op (str): The directory component got recursively by n times from the given pathname

    
`dpop(d: dict[typing.Any, typing.Any], pop: list[int | tuple[str | int | tuple] | str], de: Any = None) ‑> Any`
:   Iterate through the preferred order of precedence (`pop`) and see if
    the value exists in the dictionary. If it does, return it. If not, return
    `de`.
    
    Args:
        d (Dict[Any, Any]): Dictionary to retrieve the value from.
        pop (list[int | tuple[str | int | tuple]  |  str]): List of keys to
            iterate through.
        de (Any, optional): Default object to be returned. Defaults to None.
    
    Returns:
        Any: Retrieved value.

    
`dt(dt: str, format: str) ‑> str`
:   Remove timezone from datetime and format it to ISO 8601 format.
    
    Args:
        dt (str): Unformatted datetime string to be formatted to ISO 8601 format
        format (str): The initial format of the datetime string
    
    Returns:
        str: Formatted datetime string

    
`dt_ts(ts: str) ‑> str`
:   Convert the given unix timestamp to ISO 8601 format.
    
    Args:
        ts (str): unix timestamp to be converted to ISO 8601 format
    
    Returns:
        str: Formatted datetime string

    
`le(expr: str) ‑> Any`
:   

    
`sanitize_text(s: str)`
:
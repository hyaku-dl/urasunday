# **[ura](../index.md).[src](../src.md).[utils](utils.md)**

## **Functions**

<h3><b><a href="#func-dnrp" id="func-dnrp">dnrp</a></b></h3>

```python
(file: str, n: int = 1) ‑> str
```

Get the directory component of a pathname by n times recursively then return it.

<h3><b><i><a href="#func-dnrp-args" id="func-dnrp-args">Args:</a></i></b></h3>

- file (`str`): File to get the directory of.
- n (`int`, optional): Number of times to get up the directory???? Defaults to 1.

<h3><b><i><a href="#func-dnrp-returns" id="func-dnrp-returns">Returns:</a></i></b></h3>

`str`: The directory component got recursively by n times from the given pathname

<h3><b><a href="#func-dpop" id="func-dpop">dpop</a></b></h3>

```python
(d: dict[typing.Any, typing.Any], pop: list[int | tuple[str | int | tuple] | str], de: Any = None) ‑> Any
```

Iterate through the preferred order of precedence (`pop`) and see if the value exists in the dictionary. If it does, return it. If not, return `de`.

<h3><b><i><a href="#func-dpop-args" id="func-dpop-args">Args:</a></i></b></h3>

- d (`Dict[Any, Any]`): Dictionary to retrieve the value from.
- pop (`list[int | tuple[str | int | tuple] | str]`): List of keys to iterate through.
- de (`Any`, optional): Default object to be returned. Defaults to None.

<h3><b><i><a href="#func-dpop-returns" id="func-dpop-returns">Returns:</a></i></b></h3>

`Any`: Retrieved value.

<h3><b><a href="#func-dt" id="func-dt">dt</a></b></h3>

```python
(dt: str, format: str) ‑> str
```

Remove timezone from datetime and format it to ISO 8601 format.

<h3><b><i><a href="#func-dt-args" id="func-dt-args">Args:</a></i></b></h3>

- dt (`str`): Unformatted datetime string to be formatted to ISO 8601 format
- format (`str`): The initial format of the datetime string

<h3><b><i><a href="#func-dt-returns" id="func-dt-returns">Returns:</a></i></b></h3>

`str`: Formatted datetime string

<h3><b><a href="#func-dt_ts" id="func-dt_ts">dt_ts</a></b></h3>

```python
(ts: str) ‑> str
```

Convert the given unix timestamp to ISO 8601 format.

<h3><b><i><a href="#func-dt_ts-args" id="func-dt_ts-args">Args:</a></i></b></h3>

```
ts (str): unix timestamp to be converted to ISO 8601 format
```

<h3><b><i><a href="#func-dt_ts-returns" id="func-dt_ts-returns">Returns:</a></i></b></h3>

```
str: Formatted datetime string
```

<h3><b><a href="#func-inmd" id="func-inmd">inmd</a></b></h3>

```python
(p: str, ls: list[str] = None) ‑> str
```

"If Not `path.isdir`, Make Directories"

<h3><b><i><a href="#func-inmd-args" id="func-inmd-args">Args:</a></i></b></h3>

- p (`str`): The path to be created, if it does not exist.

<h3><b><i><a href="#func-inmd-returns" id="func-inmd-returns">Returns:</a></i></b></h3>

`str`: The path given.

<h3><b><a href="#func-ivnd" id="func-ivnd">ivnd</a></b></h3>

```python
(var: Any, de: Any) ‑> Any
```

If Var is None, return Default else var.

<h3><b><i><a href="#func-ivnd-args" id="func-ivnd-args">Args:</a></i></b></h3>

- var (`Any`): Variable to check if it is None.
- de (`Any`): Default value to return if var is None.

<h3><b><i><a href="#func-ivnd-returns" id="func-ivnd-returns">Returns:</a></i></b></h3>

`Any`: var if var is not None else de.

<h3><b><a href="#func-le" id="func-le">le</a></b></h3>

```python
(expr: str) ‑> Any
```

<h3><b><a href="#func-repl" id="func-repl">repl</a></b></h3>

```python
(s: str, repl_dict: dict[str, list[str]]) ‑> str
```

<h3><b><a href="#func-run" id="func-run">run</a></b></h3>

```python
(s: str)
```

<h3><b><a href="#func-sanitize_text" id="func-sanitize_text">sanitize_text</a></b></h3>

```python
(s: str)
```

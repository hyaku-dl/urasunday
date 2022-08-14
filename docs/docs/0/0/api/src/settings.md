# Module ura.src.settings

## Functions

`cfg(sstg) ‑> Any`
:

`cfg_path() ‑> str`
:

`readcfg(file: str) ‑> Any`
:   Read the contents of a file with the given file name.

```
Args:
    file (str): File name of the file to read the contents of.

Returns:
    Any: The contents of the file.
```

`stg(stg: str, file: str = '/home/whine/whi_ne/3/projects/personal/tools/urasunday/ura/src/stg.json') ‑> Any`
:   Retrieve dictionary value of the config file with the given file name
using recursive indexing with a string.
ex.:
Given that settings.json contains: `{"data": {"attr": {"ch": 1}}}`
`stg("data/attr/ch", "settings.json")` will return `1`

```
Args:
    stg (str): Directory of the value to be retrieved.
    file (str, optional): File name of the file to get the value from. Defaults to `path.join(dn(ap(__file__)), "settings.json")`.

Returns:
    Any: The retrieved value.
```

`wr_cfg(sstg, value) ‑> Any`
:

`wr_stg(stg: str, value: Any, file: str = '/home/whine/whi_ne/3/projects/personal/tools/urasunday/ura/src/stg.json') ‑> None`
:   Rewrite dictionary value of the config file with the given file name
using recursive indexing with a string.
ex.:
Given that settings.json contains: `{"data": {"attr": {"ch": 1}}}`
`wr_stg("data/attr/ch", 2)`
will rewrite settings.json to be: `{"data": {"attr": {"ch": 2}}}`

```
Args:
    stg (str): Directory of the value to be rewrited.
    value (Any): Value to rewrite to.
    file (str, optional): File name of the file to rewrite the value from. Defaults to path.join(dn(ap(__file__)), "settings.json").

Raises:
    FileNotFoundError: Raised if the file is not found.
```

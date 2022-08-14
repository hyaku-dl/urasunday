# Module ura.src.cfg

## Functions

`dcfg(value: dict, ext: str) ‑> str`
:   Dump the given value to a string with the given extension.

```
Args:
    value (dict): Value to dump to a string.
    ext (str): Extension to dump the value to.

Returns:
    str: The dumped value.
```

`de_rcfg()`
:

`de_wcfg(value: dict[typing.Any, typing.Any] | list[typing.Any])`
:

`pcfg(d: str, type: str) ‑> ura.src.cd.CustomDict`
:   Parse the given string as the given type.

```
Args:
    d (str): String to parse.
    type (str): Type to parse the string as.

Returns:
    CustomDict: The parsed string.
```

`rcfg(file: str) ‑> ura.src.cd.CustomDict`
:   Read the contents of a file with the given file name.

```
Args:
    file (str): File name of the file to read the contents of.

Returns:
    CustomDict: The contents of the file.
```

`wcfg(file: str, value: dict[typing.Any, typing.Any] | list[typing.Any]) ‑> None`
:   Write the given value to a file with the given file name.

```
Args:
    file (str): File name of the file to write the value to.
    value (dict[Any, Any] | list[Any]): Value to write to the file.
```

## Classes

`ExtensionNotSupported(ext: str)`
:   Method or function hasn't been implemented yet.

```
### Ancestors (in MRO)

* builtins.NotImplementedError
* builtins.RuntimeError
* builtins.Exception
* builtins.BaseException
```

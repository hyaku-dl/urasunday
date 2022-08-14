# Module ura.src.cd

## Classes

`CDInsTypeError(og_path: str, idx: int, type: type)`
:   Inappropriate argument type.

```
### Ancestors (in MRO)

* builtins.TypeError
* builtins.Exception
* builtins.BaseException
```

`CDKeyError(message: str)`
:   Mapping key not found.

```
### Ancestors (in MRO)

* builtins.KeyError
* builtins.LookupError
* builtins.Exception
* builtins.BaseException
```

`CDTypeError(message: str)`
:   Inappropriate argument type.

```
### Ancestors (in MRO)

* builtins.TypeError
* builtins.Exception
* builtins.BaseException
```

`CustomDict(*args, **kwargs)`
:   dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d\[k\] = v
dict(\*\*kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)

```
### Ancestors (in MRO)

* builtins.dict

### Methods
```

`dir(self, path: str, de: Any = None) ‑> Any`
:

`insert(self, path: str, value: Any) ‑> None`
:   Insert a value into a dictionary or list.

```
Args:
    path (str): The path to the value.
    value (Any): The value to insert.
```

`modify(self, path: str, value: Any) ‑> None`
:   Insert a value into a dictionary or list.

```
Args:
    path (str): The path to the value.
    value (Any): The value to insert.
```

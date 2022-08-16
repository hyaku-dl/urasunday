# Module ura.gui

## Functions

`connect(sid, environ)`
:

`connect_error(data)`
:

`disconnect(sid)`
:

`exp_log(sid, name: str, *msg) ‑> None`
:

`ifn(*args, **kwargs)`
:

`log(name: str, *msg) ‑> None`
:   Log message to console.

```
Args:
    msg (str): Message to be logged.
```

`log_path_fn(sid, data)`
:

`rbn(func: Callable[[Any], bool]) ‑> Callable[[Any], tuple[bool, None]]`
:   Return bool, None

```
Args:
    func (Callable[[Any], bool]): Function to be wrapped.

Returns:
    Callable[[Any], tuple[bool, None]]: Wrapped function.
```

`rta(func: Callable[[Any], Any]) ‑> Callable[[Any], tuple[True, Any]]`
:   Return True, Any

```
Args:
    func (Callable[[Any], Any]): Function to be wrapped.

Returns:
    Callable[[Any], tuple[True, Any]]: Wrapped function.
```

`rtn(func: Callable[[Any], None]) ‑> Callable[[Any], tuple[True, None]]`
:   Return True, None

```
Args:
    func (Callable[[Any], None]): Function to be wrapped.

Returns:
    Callable[[Any], tuple[True, None]]: Wrapped function.
```

`tex(func: Callable[[Any], Any]) ‑> Callable[[Any], tuple[bool, Any]]`
:   Try except wrapper

```
Args:
    func (Callable[[Any], Any]): Function to be wrapped.

Returns:
    Callable[[Any], Any]: Wrapped function.
```

## Classes

`Expose()`
:

```
### Methods
```

`config(*args, **kwargs)`
:

`dl(*args, **kwargs)`
:

`info(*args, **kwargs)`
:

`write_config(*args, **kwargs)`
:

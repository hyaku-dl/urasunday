# **[ura](index.md).[gui](gui.md)**

## **Functions**

<h3><b><a href="#func-connect" id="func-connect">connect</a></b></h3>

```python
(sid, environ)
```

<h3><b><a href="#func-connect_error" id="func-connect_error">connect_error</a></b></h3>

```python
(data)
```

<h3><b><a href="#func-disconnect" id="func-disconnect">disconnect</a></b></h3>

```python
(sid)
```

<h3><b><a href="#func-exp_log" id="func-exp_log">exp_log</a></b></h3>

```python
(sid, name: str, *msg) ‑> None
```

<h3><b><a href="#func-ifn" id="func-ifn">ifn</a></b></h3>

```python
(*args, **kwargs)
```

<h3><b><a href="#func-log" id="func-log">log</a></b></h3>

```python
(name: str, *msg) ‑> None
```

Log message to console.

<h3><b><i><a href="#func-log-args" id="func-log-args">Args:</a></i></b></h3>

- msg (`str`): Message to be logged.

<h3><b><a href="#func-log_path_fn" id="func-log_path_fn">log_path_fn</a></b></h3>

```python
(sid, data)
```

<h3><b><a href="#func-rbn" id="func-rbn">rbn</a></b></h3>

```python
(func: Callable[[Any], bool]) ‑> Callable[[Any], tuple[bool, None]]
```

Return bool, None

<h3><b><i><a href="#func-rbn-args" id="func-rbn-args">Args:</a></i></b></h3>

- func (`Callable[[Any], bool]`): Function to be wrapped.

<h3><b><i><a href="#func-rbn-returns" id="func-rbn-returns">Returns:</a></i></b></h3>

`Callable[[Any], tuple[bool, None]]`: Wrapped function.

<h3><b><a href="#func-rta" id="func-rta">rta</a></b></h3>

```python
(func: Callable[[Any], Any]) ‑> Callable[[Any], tuple[True, Any]]
```

Return True, Any

<h3><b><i><a href="#func-rta-args" id="func-rta-args">Args:</a></i></b></h3>

- func (Callable\[\[Any\], Any\]): Function to be wrapped.

<h3><b><i><a href="#func-rta-returns" id="func-rta-returns">Returns:</a></i></b></h3>

Callable\[\[Any\], tuple\[True, Any\]\]: Wrapped function.

<h3><b><a href="#func-rtn" id="func-rtn">rtn</a></b></h3>

```python
(func: Callable[[Any], None]) ‑> Callable[[Any], tuple[True, None]]
```

Return True, None

<h3><b><i><a href="#func-rtn-args" id="func-rtn-args">Args:</a></i></b></h3>

- func (`Callable[[Any], None]`): Function to be wrapped.

<h3><b><i><a href="#func-rtn-returns" id="func-rtn-returns">Returns:</a></i></b></h3>

`Callable[[Any], tuple[True, None]]`: Wrapped function.

<h3><b><a href="#func-tex" id="func-tex">tex</a></b></h3>

```python
(func: Callable[[Any], Any]) ‑> Callable[[Any], tuple[bool, Any]]
```

Try except wrapper

<h3><b><i><a href="#func-tex-args" id="func-tex-args">Args:</a></i></b></h3>

- func (Callable\[\[Any\], Any\]): Function to be wrapped.

<h3><b><i><a href="#func-tex-returns" id="func-tex-returns">Returns:</a></i></b></h3>

Callable\[\[Any\], Any\]: Wrapped function.

## **Classes**

<h3><b><a href="#class-Expose" id="class-Expose">Expose</a></b></h3>

```python
()
```

<h3><b><i><a href="#class-Expose-func" id="class-Expose-func">Methods</a></i></b></h3>

<h3><i><a href="#class-Expose-func-config" id="class-Expose-func-config">config</a></i></h3>

```python
(*args, **kwargs)
```

<h3><i><a href="#class-Expose-func-dl" id="class-Expose-func-dl">dl</a></i></h3>

```python
(*args, **kwargs)
```

<h3><i><a href="#class-Expose-func-info" id="class-Expose-func-info">info</a></i></h3>

```python
(*args, **kwargs)
```

<h3><i><a href="#class-Expose-func-write_config" id="class-Expose-func-write_config">write_config</a></i></h3>

```python
(*args, **kwargs)
```

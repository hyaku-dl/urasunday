# **[ura](../index.md).[src](../src.md).[cfg](cfg.md)**

## **Functions**

<h3><b><a href="#func-dcfg" id="func-dcfg">dcfg</a></b></h3>

```python
(value: dict, ext: str) ‑> str
```

Dump the given value to a string with the given extension.

<h3><b><i><a href="#func-dcfg-args" id="func-dcfg-args">Args:</a></i></b></h3>

- value (`dict`): Value to dump to a string.
- ext (`str`): Extension to dump the value to.

<h3><b><i><a href="#func-dcfg-returns" id="func-dcfg-returns">Returns:</a></i></b></h3>

`str`: The dumped value.

<h3><b><a href="#func-de_rcfg" id="func-de_rcfg">de_rcfg</a></b></h3>

```python
()
```

<h3><b><a href="#func-de_wcfg" id="func-de_wcfg">de_wcfg</a></b></h3>

```python
(value: dict[typing.Any, typing.Any] | list[typing.Any])
```

<h3><b><a href="#func-pcfg" id="func-pcfg">pcfg</a></b></h3>

```python
(d: str, type: str) ‑> ura.src.cd.CustomDict
```

Parse the given string as the given type.

<h3><b><i><a href="#func-pcfg-args" id="func-pcfg-args">Args:</a></i></b></h3>

- d (`str`): String to parse.
- type (`str`): Type to parse the string as.

<h3><b><i><a href="#func-pcfg-returns" id="func-pcfg-returns">Returns:</a></i></b></h3>

`CustomDict`: The parsed string.

<h3><b><a href="#func-rcfg" id="func-rcfg">rcfg</a></b></h3>

```python
(file: str) ‑> ura.src.cd.CustomDict
```

Read the contents of a file with the given file name.

<h3><b><i><a href="#func-rcfg-args" id="func-rcfg-args">Args:</a></i></b></h3>

- file (`str`): File name of the file to read the contents of.

<h3><b><i><a href="#func-rcfg-returns" id="func-rcfg-returns">Returns:</a></i></b></h3>

`CustomDict`: The contents of the file.

<h3><b><a href="#func-wcfg" id="func-wcfg">wcfg</a></b></h3>

```python
(file: str, value: dict[typing.Any, typing.Any] | list[typing.Any]) ‑> None
```

Write the given value to a file with the given file name.

<h3><b><i><a href="#func-wcfg-args" id="func-wcfg-args">Args:</a></i></b></h3>

- file (`str`): File name of the file to write the value to.
- value (`dict[Any, Any] | list[Any])`: Value to write to the file.

## **Classes**

<h3><b><a href="#class-ExtensionNotSupported" id="class-ExtensionNotSupported">ExtensionNotSupported</a></b></h3>

```python
(ext: str)
```

Method or function hasn't been implemented yet.

<h3><b><i><a href="#class-ExtensionNotSupported-mro" id="class-ExtensionNotSupported-mro">Ancestors (in MRO)</a></i></b></h3>

- builtins.NotImplementedError
- builtins.RuntimeError
- builtins.Exception
- builtins.BaseException

# **[ura](../index.md).[src](../src.md).[cli](cli.md)**

## **Functions**

<h3><b><a href="#func-command" id="func-command">command</a></b></h3>

```python
(group) ‑> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
```

Wrapper for click commands.

<h3><b><i><a href="#func-command-args" id="func-command-args">Args:</a></i></b></h3>

- group (`click.group`): Command group of the command to be under.

<h3><b><i><a href="#func-command-returns" id="func-command-returns">Returns:</a></i></b></h3>

- `Callable[[Callable[[Any], Any]], Callable[[Any], Any]]`

## **Classes**

<h3><b><a href="#class-cao" id="class-cao">cao</a></b></h3>

```python
(group, cmd: str)
```

Returns wrappers for a click command evaluated from the given arguments.

<h3><b><i><a href="#class-cao-cvar" id="class-cao-cvar">Class variables</a></i></b></h3>

`arguments`

`cmd`

`group`

<h3><b><i><a href="#class-cao-func" id="class-cao-func">Methods</a></i></b></h3>

<h3><i><a href="#class-cao-func-a" id="class-cao-func-a">a</a></i></h3>

```python
(self, f: Callable[[Any], Any]) ‑> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
```

The arguments wrapper.

<h3><a href="#class-cao-func-a-args" id="class-cao-func-a-args">Args:</a></h3>

- f (`Callable[[Any], Any]`): The command function to be decorated.

<h3><a href="#class-cao-func-a-returns" id="class-cao-func-a-returns">Returns:</a></h3>

`Callable[[Callable[[Any], Any]], Callable[[Any], Any]]`

<h3><i><a href="#class-cao-func-c" id="class-cao-func-c">c</a></i></h3>

```python
(self, f: Callable[[Any], Any]) ‑> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
```

The command wrapper.

<h3><a href="#class-cao-func-c-args" id="class-cao-func-c-args">Args:</a></h3>

- f (`Callable[[Any], Any]`): The command function to be decorated.

<h3><a href="#class-cao-func-c-returns" id="class-cao-func-c-returns">Returns:</a></h3>

`Callable[[Callable[[Any], Any]], Callable[[Any], Any]]`

<h3><i><a href="#class-cao-func-o" id="class-cao-func-o">o</a></i></h3>

```python
(self, f: Callable[[Any], Any]) ‑> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
```

The options wrapper.
My God in heaven, I'm agnostic, but please save me from all evil. Amen.

<h3><a href="#class-cao-func-o-args" id="class-cao-func-o-args">Args:</a></h3>

- f (`Callable[[Any], Any]`): The command function to be decorated.

<h3><a href="#class-cao-func-o-returns" id="class-cao-func-o-returns">Returns:</a></h3>

`Callable[[Callable[[Any], Any]], Callable[[Any], Any]]`

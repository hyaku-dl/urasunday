# **[ura](../index.md).[src](../src.md).[exceptions](exceptions.md)**

## **Functions**

<h3><b><a href="#func-c_exc" id="func-c_exc">c_exc</a></b></h3>

```python
(cls: Exception | object) ‑> Exception
```

Decorator to raise a custom exception.

This function gives the class an __init__ function that raises the exception.
If the class does not inherit from any Exception, it will be automatically inherit from Exception.
This function also wraps the Exception with `c_exc_str` method, for adding the `__str__` method.

<h3><b><i><a href="#func-c_exc-args" id="func-c_exc-args">Args:</a></i></b></h3>

- cls (`BaseException | Object`): The exception to modify.

<h3><b><i><a href="#func-c_exc-returns" id="func-c_exc-returns">Returns:</a></i></b></h3>

`BaseException`: The exception to raise.

<h3><b><a href="#func-c_exc_str" id="func-c_exc_str">c_exc_str</a></b></h3>

```python
(cls: Exception) ‑> Exception
```

Decorator to add the __str__ method to an exception.

<h3><b><i><a href="#func-c_exc_str-args" id="func-c_exc_str-args">Args:</a></i></b></h3>

- cls (`BaseException`): The exception to add the __str__ method to.

<h3><b><i><a href="#func-c_exc_str-returns" id="func-c_exc_str-returns">Returns:</a></i></b></h3>

`BaseException`: The exception to raise.

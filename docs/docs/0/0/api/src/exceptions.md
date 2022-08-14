# Module ura.src.exceptions

## Functions

`c_exc(cls: Exception | object) ‑> Exception`
:   Decorator to raise a custom exception.

```
This function gives the class an __init__ function that raises the exception.
If the class does not inherit from any Exception, it will be automatically inherit from Exception.
This function also wraps the Exception with `c_exc_str` method, for adding the `__str__` method.

Args:
    cls (BaseException | Object): The exception to modify.

Returns:
    BaseException: The exception to raise.
```

`c_exc_str(cls: Exception) ‑> Exception`
:   Decorator to add the __str__ method to an exception.

```
Args:
    cls (BaseException): The exception to add the __str__ method to.

Returns:
    BaseException: The exception to raise.
```

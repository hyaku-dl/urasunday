from functools import partial
from typing import Any

from .exceptions import c_exc, c_exc_str
from .utils import ivnd


@c_exc_str
class CDInsTypeError(TypeError):
    def __init__(self, og_path: str, idx: int, type: type) -> None:
        if type is list:
            conc = ", but is not the last element of the path."
        else:
            conc = (
                ", expected dictionary or list, if the list is the value of the "
                "last element in the path."
            )
        self.message = (
            f'`{"/".join(og_path.split("/")[:idx + 1])}` is a ' + type.__name__ + conc
        )
        super().__init__(self.message)


@c_exc
class CDKeyError(KeyError):
    pass


@c_exc
class CDTypeError(TypeError):
    pass


class CustomDict(dict):
    def __getitem__(self, key) -> Any:
        op = super().__getitem__(key)
        if op.__class__.__mro__[-2] is dict:
            return CustomDict(op)
        return op

    def _dir(
        self,
        path: str,
        cdict: dict[Any, Any] | list[Any],
        de: Any = None,
        idx: int = 0,
        og_path: str = None,
    ) -> Any:

        og_path = ivnd(og_path, path)

        path_ls = path.split("/")
        key = path_ls[0]
        tc = type(cdict)

        if len(path_ls) > 1:
            if tc.__mro__[-2] is dict:
                return self._dir(
                    path.replace(f"{key}/", ""), cdict[key], de, idx + 1, og_path
                )
            raise CDTypeError(
                f'`{"/".join(og_path.split("/")[:idx])}` is a {tc.__name__}'
                + ", expected dictionary."
            )
        else:
            try:
                return cdict.get(key, de)
            except (CDKeyError, CDTypeError):
                if de is None:
                    raise CDKeyError(
                        f'`{"/".join(og_path.split("/")[:idx + 1])}` cannot be found.'
                    )
                return de

    def dir(self, path: str, de: Any = None) -> Any:
        op = self._dir(path, self, de)
        if op.__class__.__mro__[-2] is dict:
            return CustomDict(op)
        return op

    def _insert(
        self,
        path: str,
        value: Any,
        cdict: dict[Any, Any] | list[Any],
        idx: int = None,
        og_path: str = None,
    ) -> dict[Any, Any] | list[Any]:
        """Internal function to insert a value into a dictionary or list.

        Args:
            path (str): The path to the value.
            value (Any): The value to insert.
            cdict (dict[Any, Any] | list[Any]): The dictionary to insert into.
            idx (int, optional): Depth of the current recursion. Defaults to None.
            og_path (str, optional): Original path. Used for information when raising exceptions. Defaults to None.

        Raises:
            CDInsTypeError: If the path is not fully traversed and the value is not a dictionary.

        Returns:
            dict[Any, Any] | list[Any]: The dictionary or list with the value inserted.
        """

        idx = ivnd(idx, 0)
        og_path = ivnd(og_path, path)

        tep = partial(CDInsTypeError, og_path)
        path_ls = path.split("/")
        key = path_ls[0]

        try:
            cdict[key]
        except KeyError:
            cdict[key] = {}
        tc = type(cdict)
        tck = type(cdict[key])

        if len(path_ls) > 1:
            if (tc is list) or (tc.__mro__[-2] is not dict):
                raise tep(idx, tck)
            else:
                if ((tck is list) and (len(path_ls) == 2)) or (tc.__mro__[-2] is dict):
                    op = self._insert(
                        path.replace(f"{key}/", ""), value, cdict[key], idx + 1, og_path
                    )
                    if tc.__mro__[-2] is dict:
                        cdict[key] = op
                    else:
                        cdict[key].append(op)
                    return cdict
                raise tep(idx + 1, tck)
        else:
            if tck is list:
                cdict[key].append(value)
            else:
                cdict[key] = value
            return cdict

    def insert(self, path: str, value: Any) -> None:
        """Insert a value into a dictionary or list.

        Args:
            path (str): The path to the value.
            value (Any): The value to insert.
        """
        self._insert(path, value, self)

    def _modify(
        self,
        path: str,
        value: Any,
        cdict: dict[Any, Any] | list[Any],
        idx: int = None,
        og_path: str = None,
    ) -> dict[Any, Any] | list[Any]:
        """Internal function to modify a value.

        Args:
            path (str): The path to the value.
            value (Any): The value to insert.
            cdict (dict[Any, Any] | list[Any]): The dictionary to insert into.
            idx (int, optional): Depth of the current recursion. Defaults to None.
            og_path (str, optional): Original path. Used for information when raising exceptions. Defaults to None.

        Raises:
            CDInsTypeError: If the path is not fully traversed and the value is not a dictionary.

        Returns:
            dict[Any, Any] | list[Any]: The dictionary or list with the value inserted.
        """

        idx = ivnd(idx, 0)
        og_path = ivnd(og_path, path)

        tep = partial(CDInsTypeError, og_path)
        path_ls = path.split("/")
        key = path_ls[0]

        try:
            cdict[key]
        except KeyError:
            cdict[key] = {}
        tc = type(cdict)
        tck = type(cdict[key])

        if len(path_ls) > 1:
            if (tc is list) or (tc.__mro__[-2] is not dict):
                raise tep(idx, tck)
            else:
                if ((tck is list) and (len(path_ls) == 2)) or (tc.__mro__[-2] is dict):
                    op = self._insert(
                        path.replace(f"{key}/", ""), value, cdict[key], idx + 1, og_path
                    )
                    if tc.__mro__[-2] is dict:
                        cdict[key] = op
                    else:
                        cdict[key].append(op)
                    return cdict
                raise tep(idx + 1, tck)
        else:
            cdict[key] = value
            return cdict

    def modify(self, path: str, value: Any) -> None:
        """Insert a value into a dictionary or list.

        Args:
            path (str): The path to the value.
            value (Any): The value to insert.
        """
        self._modify(path, value, self)

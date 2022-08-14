# Module ura.src.base

## Functions

`class_usi(dict_usi: dict[str, int])`
:   From the given key-value pairs of slug name and
slug index, return a class with attributes for each slug, passed to
url_slug_idx.

```
Args:
    dict_usi (dict[str, int]): The dictionary to get the slug name-index
        pairs from.

Returns:
    A class.
```

`soup(url: str, req: Type[ura.src.base.req] = ura.src.base.req, method: str = 'get', **kwargs: Dict[str, Any]) ‑> bs4.BeautifulSoup`
:   Returns a soup from the given url.

```
Args:
    url (str): URL to get the soup from.
    req (Type[req], optional): Object to call the methods from. Defaults to req.

Returns:
    BeautifulSoup: the soup
```

`urel_fn(url: str) ‑> str`
:   Turn an absolute URL to a relative one. If the given URL is already a
relative one, a URL object from the url will be returned.

```
Args:
    url (str): The URL to turn into a relative one.

Returns:
    str: The relative URL.
```

`url_slug_idx(idx: int) ‑> Callable[[str], str]`
:   From an index, get the slug from a URL whether it is a relative or an
an absolute URL.

```
Args:
    idx (int): The index of the slug from.

Returns:
    Callable[[str], str]: Method to input the URL to and get the slug.
```

## Classes

`req()`
:

```
### Class variables

`delete`
:

`get`
:

`head`
:

`options`
:

`patch`
:

`post`
:

`put`
:
```

`r()`
:

```
### Class variables

`delete`
:

`get`
:

`head`
:

`options`
:

`patch`
:

`post`
:

`put`
:
```

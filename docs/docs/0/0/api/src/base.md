# **[ura](../index.md).[src](../src.md).[base](base.md)**

## **Functions**

<h3><b><a href="#func-class_usi" id="func-class_usi">class_usi</a></b></h3>

```python
(dict_usi: dict[str, int])
```

From the given key-value pairs of slug name and slug index, return a class with attributes for each slug, passed to url_slug_idx.

<h3><b><i><a href="#func-class_usi-args" id="func-class_usi-args">Args:</a></i></b></h3>

```
dict_usi (`dict[str, int]`): The dictionary to get the slug name-index pairs from.
```

<h3><b><a href="#func-soup" id="func-soup">soup</a></b></h3>

```python
(url: str, req: Type[ura.src.base.req] = ura.src.base.req, method: str = 'get', **kwargs: Dict[str, Any]) ‑> bs4.BeautifulSoup
```

Returns a soup from the given url.

<h3><b><i><a href="#func-soup-args" id="func-soup-args">Args:</a></i></b></h3>

- url (`str`): URL to get the soup from.
- req (`Type[req]`, optional): Object to call the methods from. Defaults to req.

<h3><b><i><a href="#func-soup-returns" id="func-soup-returns">Returns:</a></i></b></h3>

`BeautifulSoup`: the soup

<h3><b><a href="#func-urel_fn" id="func-urel_fn">urel_fn</a></b></h3>

```python
(url: str) ‑> str
```

Turn an absolute URL to a relative one. If the given URL is already a
relative one, a URL object from the url will be returned.

<h3><b><i><a href="#func-urel_fn-args" id="func-urel_fn-args">Args:</a></i></b></h3>

- url (`str`): The URL to turn into a relative one.

<h3><b><i><a href="#func-urel_fn-returns" id="func-urel_fn-returns">Returns:</a></i></b></h3>

`str`: The relative URL.

<h3><b><a href="#func-url_slug_idx" id="func-url_slug_idx">url_slug_idx</a></b></h3>

```python
(idx: int) ‑> Callable[[str], str]
```

From an index, get the slug from a URL whether it is a relative or an absolute URL.

<h3><b><i><a href="#func-url_slug_idx-args" id="func-url_slug_idx-args">Args:</a></i></b></h3>

- idx (`int`): The index of the slug from.

<h3><b><i><a href="#func-url_slug_idx-returns" id="func-url_slug_idx-returns">Returns:</a></i></b></h3>

`Callable[[str], str]`: Method to input the URL to and get the slug.

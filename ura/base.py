import time
from functools import partial
from typing import Any
from typing import Callable
from typing import Callable as callable
from typing import Dict, List, Type

import httpx
from bs4 import BeautifulSoup
from yarl import URL

METHODS = ["get", "options", "head", "post", "put", "patch", "delete"]
SESSION = httpx.Client()

def urel_fn(url: str) -> str:
    """Turn an absolute URL to a relative one. If the given URL is already a
    relative one, a URL object from the url will be returned.

    Args:
        url (str): The URL to turn into a relative one.

    Returns:
        str: The relative URL.
    """
    url = URL(url)
    if url.is_absolute():
        url = url.relative()
    return url

def url_slug_idx(idx: int) -> callable[[str], str]:
    """From an index, get the slug from a URL whether it is a relative or an
    an absolute URL.

    Args:
        idx (int): The index of the slug from.

    Returns:
        callable[[str], str]: Method to input the URL to and get the slug.
    """

    def _inner(url: str) -> str:
        """The returned method where to input the URL to and get the slug from.

        Args:
            url (str): The URL to get the slug from.

        Returns:
            str: The slug.
        """
        urel = urel_fn(url)
        return urel.parts[idx + 1]

    return _inner

def class_usi(dict_usi: dict[str, int]):
    """From the given key-value pairs of slug name and
    slug index, return a class with attributes for each slug, passed to
    url_slug_idx.

    Args:
        dict_usi (dict[str, int]): The dictionary to get the slug name-index
            pairs from.

    Returns:
        A class.
    """

    class _class:
        """The class to return."""
    for k, v in dict_usi.items():
        setattr(_class, k, url_slug_idx(v))
    return _class

def _req(
        url: str,
        ra: Callable[[httpx.Response], int]=None,
        method: str = "get",
        session: httpx.Client = SESSION,
        *args: List[Any],
        **kwargs: Dict[str, Any]
    ) -> httpx.Response:
    """Custom request function with retry after capabilities for 429s.

    Args:
        url (str): URL to send the request to.
        ra (Callable[[httpx.Response], int], optional): Retry after function,
            receives the Response object and returns the seconds before
            retrying. Defaults to None.
        method (str, optional): The request method. Defaults to "get".
        session (httpx.Client, optional): Session client. Defaults to SESSION.

    Returns:
        httpx.Response: Response object.
    """
    resp = getattr(session, method)(url, follow_redirects=True, *args, **kwargs)
    if resp.status_code == 429:
        if ra is not None:
            time.sleep(ra(resp))
            return _req(url, ra, method, session, *args, **kwargs)
    return resp

class req:
    pass

req_dict = {
    req: {},
}

for r, kw in req_dict.items():
    for i in METHODS:
        setattr(r, i, partial(_req, method=i, **kw))

def soup(url: str, req: Type[req]=req, method: str="get", **kwargs: Dict[str, Any]) -> BeautifulSoup:
    """Returns a soup from the given url.

    Args:
        url (str): URL to get the soup from.
        req (Type[req], optional): Object to call the methods from. Defaults to req.

    Returns:
        BeautifulSoup: the soup
    """
    return BeautifulSoup(getattr(req, method)(url, **kwargs).text, "lxml")
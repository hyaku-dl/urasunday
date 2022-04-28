import asyncio
import json
import os
import os.path
import re
import shutil
import time
from typing import Any, Callable, Dict, List

import aiofiles
from tqdm.asyncio import tqdm_asyncio

from ura.settings import cfg
from ura.utils import sanitize_text

from .base import class_usi, req, soup

USI = class_usi({
    "ch_id": 2,
})

class DownloadFailed(Exception):
    pass

def sanitize_filename(filename: str) -> str:
    """
    Sanitize the given filename.

    Args:
        filename (str): The filename to be sanitized.

    Returns:
        str: Sanitized filename.
    """
    return re.sub(re.compile(r"[<>:\"/\\|?*]", re.DOTALL), "", str(filename))


def get_extension(filename: str) -> str:
    """
    Get the file extension of a file from the given filename.

    Args:
        filename (str): The filename to get the file extension from.

    Returns:
        str: The file extension from the given filename.
    """
    return filename.strip("/").split("/")[-1].split("?")[0].split(".")[-1]

def ordinal(n: int) -> str:
    """
    Convert the given number to ordinal number.

    Args:
        n (int): The number to convert into ordinal number.

    Returns:
        str: The said ordinal number.
    """
    return "%d%s" % (n, "tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

def _cr(rs: str):
    """
    The function that calculates the range.

    Args:
        rs (str): The range string where the range is calculated from.

    Yields:
        Callable[[Any], bool]: The function that checks if the given int is within the range or not.
    """

    for matches in re.finditer(r"(?:(-?[0-9.]*)[:](-?[0-9.]*)|(-?[0-9.]+))", rs):
        start, end, singular = matches.groups()
        if (start and end) and float(start) > float(end):
            start, end = end, start
        yield (lambda x, s=singular: float(s) == x) if singular else (lambda x: True) if not (start or end) else (lambda x, s=start: x >= float(s)) if start and not end else (lambda x, e=end: x <= float(e)) if not start and end else (lambda x, s=start, e=end: float(s) <= x <= float(e))
    if not rs:
        return lambda *args, **kwargs: True

def cr(rs: str) -> Callable[[int], bool]:
    """
    Returns a function that checks if the given int is within the range or not.
    The range is calculated from the given string.

    Args:
        rs (str): The range string where the range is calculated from.

    Returns:
        Callable[[int], bool]: The function that checks if the given int is within the range or not.
    """


    if rs:
        return lambda x: any(condition(x) for condition in _cr(rs))
    else:
        return lambda x: True

class Downloader:
    def __init__(
        self,
        directory: str=None,
        overwrite: bool=True,
        **kwargs: Dict[str, Any]
    ):
        local = locals()
        for i in ["overwrite",]:
            setattr(self, i, local[i])
        if directory:
            self.ddir = directory
        else:
            self.ddir = cfg("download_dir")

    async def _dlf(self, file: list[str], n: int=0):
        """
        The core individual image downloader.
        Args:
            file (str): List containing the filename and the url of the file.
            n (int, optional): Times the download for this certain file is retried. Defaults to 0.
        """
        async with aiofiles.open(file[0] + ".tmp", 'wb') as f:
            r = req.get(file[1])
            if r.status_code == 200:
                async for data in r.aiter_bytes():
                    await f.write(data)
            elif r.status_code == 429:
                time.sleep(5)
                await self._dlf(file, n)

    async def dlf(self, file: List[str]) -> None:
        """
        Individual image downloader.
        Args:
            file (str): List containing the filename and the url of the file.
        """
        try:
            os.makedirs(os.path.split(file[0])[0])
        except FileExistsError:
            pass
        if os.path.isfile(f"{file[0]}.tmp"):
            os.remove(f"{file[0]}.tmp")
        await self._dlf(file)
        os.replace(f"{file[0]}.tmp", file[0])

    async def _dlch(self, manga: str, chapter: str, urls: List[str], n: int=0):
        # """
        # Individual chapter downloader.
        # Args:
        #     k (Union[int, float]): Chapter number.
        #     v (List[str]): List of image urls.
        # """
        dl = True
        jdir = os.path.join(self.ddir, manga, sanitize_filename(chapter))
        if os.path.isdir(jdir):
            if self.overwrite:
                shutil.rmtree(jdir)
            else:
                dl = False
        if dl:
            dl = True
            if dl:
                files = []
                for index, page in enumerate(urls):
                    filename = os.path.join(
                        self.ddir,
                        manga,
                        sanitize_filename(chapter),
                        f"{index}.{get_extension(str(page))}"
                    ).replace("\\", "/")
                    files.append((filename, page))
                fmt = chapter + " [{remaining_s:05.2f} secs, {rate_fmt:0>12}] " + "{bar}" +" [{n:03d}/{total:03d}, {percentage:03.0f}%]"
                try:
                    await tqdm_asyncio.gather(
                        *[self.dlf(file) for file in files],
                        total=len(files),
                        leave=True,
                        unit=" img",
                        disable=False,
                        dynamic_ncols=True,
                        smoothing=1,
                        bar_format=fmt
                    )
                except DownloadFailed as e:
                    raise e

    def dlch(self, url: str):
        RP = r"const pages = \[(\s.+?)+?\s+\];"

        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        }

        resp = req.get(url, headers=headers)
        wrong_json = re.search(RP, resp.text).group(0)[14:-1].replace("'", '"')
        wrong_json = re.sub(r"(.+?): ", r'"\1": ', wrong_json)
        wrong_json = re.sub(r'\",\s+}', r'"}', wrong_json)
        pages = re.sub(r'\},\s+]', r'}]', wrong_json)

        ms = soup(url)
        title = sanitize_text(ms.select_one("div.info h1").text)
        chapter = sanitize_text(ms.select_one("div.title div div").text)

        urls = [i["src"] for i in json.loads(pages)]
        asyncio.get_event_loop().run_until_complete(
            self._dlch(title, f'{USI.ch_id(url)} - {chapter}', urls)
        )
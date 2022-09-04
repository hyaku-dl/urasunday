import asyncio
import json
import os
import re
import shutil
import time
from typing import Any, Dict, List

import aiofiles
from tqdm.asyncio import tqdm_asyncio

try:
    from .base import class_usi, req, soup
    from .cfg import de_rcfg
    from .utils import sanitize_text
except ImportError:
    from base import class_usi, req, soup
    from cfg import de_rcfg
    from utils import sanitize_text

# Constants
USI = class_usi(
    {
        "ch_id": 2,
    }
)


def get_stg(path: str, de: Any = None):
    return de_rcfg().dir(path, de)


def sanitize_filename(filename: str) -> str:
    """Sanitize the given filename.

    Args:
    - filename (`str`): The filename to be sanitized.

    Returns:
    `str`: Sanitized filename.
    """
    return re.sub(re.compile(r"[<>:\"/\\|?*]", re.DOTALL), "", str(filename))


def get_extension(filename: str) -> str:
    """
    Get the file extension of a file from the given filename.

    Args:
    - filename (`str`): The filename to get the file extension from.

    Returns:
    `str`: The file extension from the given filename.
    """
    return filename.strip("/").split("/")[-1].split("?")[0].split(".")[-1]


class Downloader:
    def __init__(
        self, directory: str = None, overwrite: bool = None, **kwargs: Dict[str, Any]
    ):
        local = locals()
        for k, v in {
            "directory": ["ddir", "download_dir"],
            "overwrite": ["overwrite", "overwrite"],
        }.items():
            gs_var = get_stg(v[1])
            if gs_var is None:
                op = local[k]
            else:
                op = gs_var
            setattr(self, v[0], op)

    async def _dlf(self, file: list[str], n: int = 0):
        """The core individual image downloader.

        Args:
        - file (`str`): List containing the filename and the url of the file.
        - n (`int`, optional): Times the download for this certain file is retried. Defaults to 0.
        """
        async with aiofiles.open(file[0] + ".tmp", "wb") as f:
            r = req.get(file[1])
            if r.status_code == 200:
                async for data in r.aiter_bytes():
                    await f.write(data)
            elif r.status_code == 429:
                time.sleep(5)
                await self._dlf(file, n)

    async def dlf(self, file: List[str]):
        """
        Individual image downloader.
        Args:
        - file (`str`): List containing the filename and the url of the file.
        """
        try:
            os.makedirs(os.path.split(file[0])[0])
        except FileExistsError:
            pass
        if os.path.isfile(f"{file[0]}.tmp"):
            os.remove(f"{file[0]}.tmp")
        await self._dlf(file)
        os.replace(f"{file[0]}.tmp", file[0])

    async def _dlch(self, manga: str, chapter: str, urls: List[str], n: int = 0):
        dl = True
        self.jdir = jdir = os.path.join(self.ddir, manga, sanitize_filename(chapter))
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
                        f"{index}.{get_extension(str(page))}",
                    ).replace("\\", "/")
                    files.append((filename, page))
                fmt = (
                    chapter
                    + " [{remaining_s:05.2f} secs, {rate_fmt:0>12}] "
                    + "{bar}"
                    + " [{n:03d}/{total:03d}, {percentage:03.0f}%]"
                )
                await tqdm_asyncio.gather(
                    *[self.dlf(file) for file in files],
                    total=len(files),
                    leave=True,
                    unit=" img",
                    disable=False,
                    dynamic_ncols=True,
                    smoothing=1,
                    bar_format=fmt,
                )

    def dlch(self, url: str):
        RP = r"const pages = \[(\s.+?)+?\s+\];"

        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        }

        resp = req.get(url, headers=headers)
        wrong_json = re.search(RP, resp.text).group(0)[14:-1].replace("'", '"')
        wrong_json = re.sub(r"(.+?): ", r'"\1": ', wrong_json)
        wrong_json = re.sub(r"\",\s+}", r'"}', wrong_json)
        pages = re.sub(r"\},\s+]", r"}]", wrong_json)

        ms = soup(url)
        title = sanitize_text(ms.select_one("div.info h1").text)
        chapter = sanitize_text(ms.select_one("div.title div div").text)

        urls = [i["src"] for i in json.loads(pages)]
        asyncio.get_event_loop().run_until_complete(
            self._dlch(title, f"{USI.ch_id(url)} - {chapter}", urls)
        )

        return self.jdir

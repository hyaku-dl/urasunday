import json
import re
from os import path

from rich.pretty import pprint as print

from ura.base import class_usi, req, soup
from ura.utils import sanitize_text

# from ura.download import Downloader

USI = class_usi({
    "ch_id": 2,
})

url = "https://urasunday.com/title/1301/184432"
RP = r"const pages = \[(\s.+?)+?\s+\];"
RT = r""

headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
}

resp = req.get(url, headers=headers)
wrong_json = re.search(RP, resp.text).group(0)[14:-1].replace("'", '"')
wrong_json = re.sub(r"(.+?): ", r'"\1": ', wrong_json)
wrong_json = re.sub(r'\",\s+}', r'"}', wrong_json)
pages = re.sub(r'\},\s+]', r'}]', wrong_json)

print([i["src"] for i in json.loads(pages)])

ms = soup(url)
title = sanitize_text(ms.select_one("div.info h1").text)
chapter = sanitize_text(ms.select_one("div.title div div").text)
print(path.join(title, f'{USI.ch_id(url)} - {chapter}'))

# Downloader()
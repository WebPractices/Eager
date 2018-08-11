# coding=utf-8
import asyncio
import aiohttp
import requests
from requests.exceptions import ConnectionError


def parse_url(url, code='utf-8',params=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    if params and isinstance(params, dict):
        for k, v in params.items():
            headers[k] = v
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            resp.encoding = code
            return resp.text
        return None
    except ConnectionError:
        print('Error.')
    return None

class Downloader(object):
    """async crawler"""
    def __init__(self, urls):
        self.urls = urls
        self._htmls = []

    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                self._htmls.append(await resp.text())

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))

    @property
    def htmls(self):
        self.download()
        return self._htmls

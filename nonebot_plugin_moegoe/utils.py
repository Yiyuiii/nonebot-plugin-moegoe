from typing import Optional
from pathlib import Path
import httpx
from gradio_client import Client


class GradioClients:
    def __init__(self):
        self.client_dict = dict()

    def forward(self, url: str, *args, **kwargs):
        '''
        :param url: api url
        :return: stat, wav_path
        '''
        if url not in self.client_dict.keys():
            self.client_dict[url] = Client(url)
        result = self.client_dict[url].predict(*args, **kwargs)
        return result


async def download_url(url: str) -> Optional[bytes]:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=5)
                resp.raise_for_status()
                return resp.content
            except Exception:
                pass
    return None


def write_file(path: Path, data, binary=True):
    path.parent.mkdir(parents=True, exist_ok=True)
    if binary:
        path.write_bytes(data)
    else:
        path.write_text(data, encoding='UTF-8')

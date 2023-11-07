from typing import Optional
from pathlib import Path
import httpx


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

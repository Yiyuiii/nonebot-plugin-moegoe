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


def write_file(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(data)

def versionGreater(v1: str, v2: str):
    n1 = v1.split('.')
    n2 = v2.split('.')
    for i in range(min(len(n1), len(n2))):
        if int(n1[i]) > int(n2[i]):
            return True
        if int(n1[i]) < int(n2[i]):
            return False
    return False

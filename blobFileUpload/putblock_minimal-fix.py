import os
import asyncio
import aiofiles
import logging
from pathlib import Path
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import StandardBlobTier

CONN_STR   = os.environ.get("AZURE_STORAGE_CONNECTION_STRING", "<your-conn-string>")
CONTAINER  = os.environ.get("AZURE_CONTAINER", "<your-container>")
LOCAL_FILE = os.environ.get("LOCAL_FILE", "/path/to/large.file") 
DEST_PREFIX = os.environ.get("DEST_PREFIX", "snapshots")
MAX_CONC   = int(os.environ.get("MAX_CONCURRENCY", "16"))
BLOB_TIER  = os.environ.get("BLOB_TIER")

logging.basicConfig(level=logging.INFO)
logging.getLogger("azure").setLevel(logging.INFO)

class AsyncNoSeek:
    def __init__(self, f): self._f = f
    async def read(self, n=-1): return await self._f.read(n)
    def seekable(self): return False

async def main():
    bsc = BlobServiceClient.from_connection_string(CONN_STR, max_block_size=20 * 1024 * 1024)
    container = bsc.get_container_client(CONTAINER)

    name = f"{DEST_PREFIX.rstrip('/')}/{Path(LOCAL_FILE).name}"
    size = os.stat(LOCAL_FILE).st_size
    async with aiofiles.open(LOCAL_FILE, "rb") as data:
        wrapper = AsyncNoSeek(data)
        await container.upload_blob(
            name=name,
            data=wrapper,
            length=size,
            overwrite=True,
            max_concurrency=MAX_CONC,
            standard_blob_tier=StandardBlobTier(BLOB_TIER.capitalize()) if BLOB_TIER else None,
        )
    print("DONE:", name)

if __name__ == "__main__":
    asyncio.run(main())

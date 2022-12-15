import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from starlite.cache import CacheBackendProtocol


class JSONCacheBackend(CacheBackendProtocol):
    def __init__(self, path: os.PathLike):
        self._persistence_path = path
        try:
            data = json.loads(Path(path).read_text())
            print("Got here")
            self.store = data["store"]
            self.timestamps = data["timestamps"]
        except FileNotFoundError:
            self.store = {}
            self.timestamps = {}

    async def get(self, key: str) -> Any:
        timestamp = self.timestamps.get(key)
        if timestamp is not None:
            time = datetime.fromisoformat(timestamp)
            if time < time.utcnow():
                del self.timestamps[key]
                del self.store[key]
                return None
        return self.store.get(key)

    async def set(self, key: str, value: Any, expiration: int) -> None:
        self.store[key] = value
        self.timestamps[key] = (
            datetime.utcnow() + timedelta(seconds=expiration)
        ).isoformat()
        self._persist()

    async def delete(self, key: str) -> None:
        del self.store[key]
        del self.timestamps[key]
        self._persist()

    def _persist(self) -> None:
        self._persistence_path.write_text(json.dumps({
            "store": self.store,
            "timestamps": self.timestamps
        }))

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

    def get(self, key: str) -> Any:
        timestamp = self.timestamps.get(key)
        if timestamp is not None:
            time = datetime.fromisoformat(timestamp)
            if time < time.utcnow():
                return None
        return self.store.get(key)

    def set(self, key: str, value: Any, expiration: int) -> None:
        self.store[key] = value
        self.timestamps[key] = (
            datetime.utcnow() + timedelta(seconds=expiration)
        ).isoformat()

    def delete(self, key: str) -> None:
        del self.store[key]
        del self.timestamps[key]

    def __del__(self):
        Path(self._persistence_path).write(
            json.dumps({"store": self.store, "timestamps": self.timestamps})
        )

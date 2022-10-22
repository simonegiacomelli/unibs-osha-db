import json
import traceback
from abc import ABC
from pathlib import Path
from typing import Callable

from cache.version_descriptor import VersionDescriptor


class CacheABC(ABC):
    folder: Path
    prefix: str

    def path_for(self, filename_suffix) -> Path:
        pass

    def delete(self):
        pass


class Cache(CacheABC):

    def __init__(self, prefix_path: Path):
        super().__init__()

        self.folder = prefix_path.parent
        self.prefix = prefix_path.name

    def path_for(self, filename_suffix) -> Path:
        return self.folder / (self.prefix + '.' + filename_suffix)

    def delete(self):
        for f in self.folder.glob(self.prefix + '.*'):
            f.unlink()

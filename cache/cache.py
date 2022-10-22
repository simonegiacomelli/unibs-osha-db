from abc import ABC
from pathlib import Path

from cache.path_ext import PathExt


class CacheABC(ABC):
    folder: Path
    prefix: str

    def path_for(self, filename_suffix) -> PathExt:
        pass

    def delete(self):
        pass


class Cache(CacheABC):

    def __init__(self, prefix_path: Path):
        super().__init__()

        self.folder = prefix_path.parent
        self.prefix = prefix_path.name

    def path_for(self, filename_suffix) -> PathExt:
        return PathExt(self.folder / (self.prefix + '.' + filename_suffix))

    def delete(self):
        for f in self.folder.glob(self.prefix + '.*'):
            f.unlink()

import json
import traceback
from abc import ABC
from pathlib import Path
from typing import Callable

from cache.version_descriptor import VersionDescriptor


class Cache_ABC(ABC):
    folder: Path
    prefix: str
    version_factory: Callable[[], VersionDescriptor]
    current_version: Callable[[], VersionDescriptor]

    def path_for(self, filename_suffix) -> Path:
        pass

    def is_valid(self) -> bool:
        pass

    def set_valid(self):
        pass

    def delete(self):
        pass


class Cache(Cache_ABC):

    def __init__(self, folder: Path, prefix: str,
                 current_version: Callable[[], VersionDescriptor]):
        super().__init__()
        self.current_version = current_version
        self.folder = folder
        self.prefix = prefix
        self.path_version = self.path_for('version.json')

    def path_for(self, filename_suffix) -> Path:
        return self.folder / (self.prefix + '.' + filename_suffix)

    def set_valid(self):
        version = self.current_version()
        self.path_version.write_text(version.json())

    def is_valid(self) -> bool:
        if not self.path_version.exists():
            return False

        try:
            current_ver = self.current_version()
            current_ver_str = current_ver.json()
            current_ver_obj = json.loads(current_ver_str)
            cached_version_obj = json.loads(self.path_version.read_text())
            return current_ver_obj == cached_version_obj
        except Exception:
            print(traceback.format_exc())
            return False

    def delete(self):
        for f in self.folder.glob(self.prefix + '.*'):
            f.unlink()

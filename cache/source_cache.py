import json
from pathlib import Path
from typing import Optional, Generic, Callable

from cache.versioned_cache import VersionedCache
from cache.source import Source, T
from cache.version_descriptor import VersionDescriptor


class SourceCache(Source, Generic[T]):
    def __init__(self, source: Source, prefix_path: Path):
        super().__init__(source.name, source.kind + '-CACHED', source.constructor)
        self.source = source
        self.cache = VersionedCache(prefix_path, source.version)

    def data(self) -> Optional[T]:
        self._load_internal()
        data_path = self._cache_data_path()
        if data_path.exists():
            json_text = data_path.read_text()
            data_args = json.loads(json_text)
            return self.constructor(**data_args)
        return None

    def version(self) -> VersionDescriptor:
        return self.source.version()

    def load_errors(self):
        self._load_internal()

    def cache_delete(self):
        self.cache.delete()

    def _cache_data_path(self) -> Path:
        return self.cache.path_for('data.json')

    def _cache_errors_path(self) -> Path:
        return self.cache.path_for('errors.json')

    def _load_internal(self):
        self.errors.clear()
        data_path = self._cache_data_path()
        errs_path = self._cache_errors_path()
        if self.cache.is_valid():
            if errs_path.exists():
                loaded = json.loads(errs_path.read_text())
                self.errors.extend(loaded)
            return

        data_path.unlink(missing_ok=True)
        errs_path.unlink(missing_ok=True)

        data = self.source.data()
        self.errors.extend(self.source.errors)

        if len(self.errors) > 0:
            errs_path.write_text(json.dumps(self.errors))
        else:
            data_path.write_text(data.json())

        self.cache.set_valid()


def source_wrap(source: Source[T], prefix_path: Path) -> SourceCache[T]:
    if isinstance(source, SourceCache):
        return source

    return SourceCache(source, prefix_path)


def source_unwrap(source: Source) -> Source:
    if isinstance(source, SourceCache):
        return source.source

    return source

import json
import pathlib
from typing import Type

from cache.source import T


class PathExt(pathlib.Path):
    _flavour = type(pathlib.Path())._flavour

    def __init__(self, *args, **kwargs):
        super().__init__()

    def serialize_json(self, instance: T):
        self.write_text(instance.json())

    def deserialize_json(self, pydantic_type: Type[T]) -> T:
        args = json.loads(self.read_text())
        return pydantic_type(**args)

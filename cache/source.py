from abc import ABC
from typing import List, Optional, TypeVar, Generic, Callable, Type

from pydantic import BaseModel

from cache.version_descriptor import VersionDescriptor, VD_Numbered

T = TypeVar("T", bound=BaseModel)


class Source(ABC, Generic[T]):
    def __init__(self, name: str, kind: str, constructor: Type[T]):
        self.constructor = constructor
        self.kind = kind
        self.name = name
        self.errors: List[str] = []

    def data(self) -> Optional[T]:
        """
        This should clear the errors and try to return the data.

        @return:
         - if errors result should be None
         - if no errors result should be valid data
         """
        pass

    def version(self) -> VersionDescriptor:
        """
        It should collect the data source (e.g, one VD_FileAttr for each csv or xls file)
        This method should be very fast and very light on resource consumption
        @return:
        """
        return VD_Numbered(version=1)

    def load_errors(self):
        self.data()

    def cache_delete(self):
        pass

    @property
    def errors_str(self) -> str:
        errors = self.errors
        res = f'Errors found {len(errors)}, name `{self.name}`\n'
        for e in errors:
            res += f'  {e}\n'
        return res

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def raise_if_errors(self):
        if self.has_errors:
            raise Exception(self.errors_str)

    def __repr__(self):
        return f'{self.kind}({self.name})'

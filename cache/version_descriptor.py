import os
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import TypeVar, List, Union

from pydantic import BaseModel

from core.hashlib import md5sum

VersionDescriptor = TypeVar('VersionDescriptor', bound=BaseModel)


class VD_Numbered(BaseModel):
    version: int


class VD_List(BaseModel):
    descriptors: List[VersionDescriptor]

    @staticmethod
    def new(*descriptors: VersionDescriptor) -> 'VD_List':
        return VD_List(descriptors=list(descriptors))


class VD_FileHash(BaseModel):
    filename: str
    md5_hash: str

    @staticmethod
    def new(path: Union[str, PathLike]) -> 'VD_FileHash':
        p = Path(path)
        h = md5sum(p)
        return VD_FileHash(
            filename=p.name,
            md5_hash=h
        )


class VD_FileAttr(BaseModel):
    filename: str
    modified: datetime
    changed: datetime
    size: int

    @staticmethod
    def new(path: Union[str, PathLike]) -> 'VD_FileAttr':
        p = Path(path)
        stat = os.stat(p)
        return VD_FileAttr(
            filename=p.name,
            modified=stat.st_mtime,
            changed=stat.st_ctime,
            size=stat.st_size
        )

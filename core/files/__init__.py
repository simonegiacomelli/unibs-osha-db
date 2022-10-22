import os
from os import PathLike
from pathlib import Path
from typing import Union


def dir_empty(path: Union[PathLike, str]) -> bool:
    path = Path(path)
    assert path.is_dir()
    return len(os.listdir(path)) == 0

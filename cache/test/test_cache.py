import shutil
import unittest
from pathlib import Path
from typing import Callable

from core.files import dir_empty
from cache.cache import Cache, Cache_ABC
from cache.version_descriptor import VersionDescriptor, VD_Numbered, VD_List

v1 = VD_Numbered(version=1)


class Test_Cache(unittest.TestCase):

    def test_emptyCacheFolder_shouldBeNotValid(self):
        target = self.new_target()
        self.assertFalse(target.is_valid())

    def test_readShouldReturn_equalDataframe(self):
        target = self.new_target()
        target.path_for('dataframe.txt').write_text('123')
        target.set_valid()
        self.assertTrue('123', target.path_for('dataframe.txt').read_text())

    def test_shouldBeValid(self):
        target = self.new_target()
        target.set_valid()
        self.assertTrue(target.is_valid())

    def test_differentVersion_shouldNotBeValid(self):
        version = 1

        def cache_version():
            return VD_Numbered(version=version)

        target = self.new_target(cache_version)
        version = 2
        self.assertFalse(target.is_valid())

    def test_differentVersionComplexTypes_shouldBeValid(self):
        def cache_version():
            return VD_List.new(v1)

        target = self.new_target(cache_version)
        target.set_valid()
        self.assertTrue(target.is_valid())

    def test_delete_shouldRemoveAllPrefix(self):
        target = self.new_target()
        target.path_for('pluto').write_text('something')
        target.delete()
        self.assertTrue(dir_empty(target.folder))

    def new_target(self, current_version: Callable[[], VersionDescriptor] = lambda: v1) -> Cache_ABC:
        tmp1 = _tmp_folder('tmp1')
        target = Cache(tmp1 / 'foo', current_version)
        return target


if __name__ == '__main__':
    unittest.main()

parent = Path(__file__).parent


def _tmp_folder(name) -> Path:
    res = parent / 'tmp' / name
    _clean_folder(res)
    return res


def _clean_folder(tmp: Path) -> Path:
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)
    return tmp

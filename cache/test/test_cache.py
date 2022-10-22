import unittest
from pathlib import Path

from cache.cache import Cache, CacheABC
from cache.test.test_versioned_cache import _tmp_folder
from core.files import dir_empty


class TestCache(unittest.TestCase):

    def test_readShouldReturn_equalDataframe(self):
        target = self.new_target()
        target.path_for('dataframe.txt').write_text('123')
        self.assertTrue('123', target.path_for('dataframe.txt').read_text())

    def test_delete_shouldRemoveAllPrefix(self):
        target = self.new_target()
        target.path_for('pluto').write_text('something')
        target.delete()
        self.assertTrue(dir_empty(target.folder))

    def new_target(self) -> CacheABC:
        tmp1 = _tmp_folder('tmp1')
        target = Cache(tmp1 / 'foo')
        return target


if __name__ == '__main__':
    unittest.main()

parent = Path(__file__).parent

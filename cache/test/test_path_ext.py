import unittest
from pathlib import Path

from pydantic import BaseModel

from cache.path_ext import PathExt
from cache.test.test_versioned_cache import _tmp_folder


class TestPathExt(unittest.TestCase):

    def test_1(self):
        target = self.new_target()
        target.serialize_json(MockData(n=1))
        instance = target.deserialize_json(MockData)
        self.assertEqual(1, instance.n)

    def new_target(self) -> PathExt:
        tmp1 = _tmp_folder('tmp1')
        target = PathExt(tmp1 / 'foo')
        return target


class MockData(BaseModel):
    n: int


if __name__ == '__main__':
    unittest.main()

parent = Path(__file__).parent

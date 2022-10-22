import unittest
from typing import Generic, Callable, Optional

from pydantic import BaseModel

from cache.source import Source, T
from cache.source_cache import source_wrap
from cache.test.test_versioned_cache import _tmp_folder


class TestSourceCache(unittest.TestCase):
    def test_should_return_underling_data(self):
        tmp_folder = _tmp_folder('source_cache') / 'test1'
        data = MockData(n=1)
        target = source_wrap(MockSource('source1', data), tmp_folder)

        self.assertEqual(1, target.data().n)

        # changing underling data should not be reflected in target because of cache

        data.n = 2
        self.assertEqual(1, target.data().n)


class MockData(BaseModel):
    n: int


class MockSource(Source[MockData]):
    def __init__(self, name: str, mock_data: MockData):
        super().__init__(name, 'mock-source', MockData)
        self.mock_data = mock_data

    def data(self) -> Optional[MockData]:
        return self.mock_data

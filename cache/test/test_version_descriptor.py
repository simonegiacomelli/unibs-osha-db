import unittest
from pathlib import Path

from cache.version_descriptor import VD_Numbered, VD_FileHash, VD_List, VD_FileAttr

file1 = Path(__file__)
file2 = file1.parent.parent / 'version_descriptor.py'


class TestVersionDescriptor(unittest.TestCase):

    def test_VD_Numbered__should_satisfy_equality(self):
        self.assertEqual(VD_Numbered(version=1), VD_Numbered(version=1))
        self.assertNotEqual(VD_Numbered(version=1), VD_Numbered(version=2))

    def test_VD_FileHash__should_satisfy_equality(self):
        self.assertEqual(VD_FileHash.new(file1), VD_FileHash.new(file1))
        self.assertNotEqual(VD_FileHash.new(file1), VD_FileHash.new(file2))

    def test_VD_FileAttr__should_satisfy_equality(self):
        self.assertEqual(VD_FileAttr.new(file1), VD_FileAttr.new(file1))
        self.assertNotEqual(VD_FileAttr.new(file1), VD_FileAttr.new(file2))

    def test_VD_List__should_satisfy_equality(self):
        self.assertEqual(
            VD_List.new(VD_FileHash.new(file1), VD_Numbered(version=1)),
            VD_List.new(VD_FileHash.new(file1), VD_Numbered(version=1))
        )

        self.assertNotEqual(
            VD_List.new(VD_FileHash.new(file1), VD_Numbered(version=1)),
            VD_List.new(VD_FileHash.new(file1), VD_Numbered(version=2))
        )

        self.assertNotEqual(
            VD_List.new(VD_Numbered(version=1), VD_FileHash.new(file1)),
            VD_List.new(VD_FileHash.new(file1), VD_Numbered(version=1))
        )


if __name__ == '__main__':
    unittest.main()

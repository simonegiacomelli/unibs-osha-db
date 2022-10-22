import unittest

from osha.detail_page import DetailData
from osha.test.test_data.folder_structure import folder_structure


class TestInstanceList(unittest.TestCase):

    def test_box_count(self):
        target = self._target('office-0100000-index-000000-detail.html')
        self.assertEqual(20, len(target.boxes))

    def test_box_count_bis(self):
        target = self._target('nine-boxes.html')
        self.assertEqual(9, len(target.boxes))

    def test_complex_box(self):
        target = self._target('complex-box.html')
        self.assertEqual(1, len(target.boxes))
        box = target.boxes[0]
        pass

    def _target(self, html) -> DetailData:
        path = (folder_structure.detail_pages / html)
        target = DetailData()
        target.load_from_html(path.read_text())

        return target

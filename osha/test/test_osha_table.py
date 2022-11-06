import unittest

from osha.osha_table import OshaTable
from osha.test.test_data.folder_structure import folder_structure


class TestAccidentDetail(unittest.TestCase):

    def disabled_test_complex_box(self):
        target = self._target('complex-box.html')
        self.assertEqual(2, len(target.content_tables))

    def _target(self, html) -> OshaTable:
        path = (folder_structure.detail_pages / html)
        target = OshaTable()
        target.load_from_html(path.read_text())

        return target

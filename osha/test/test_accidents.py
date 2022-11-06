import unittest
from typing import List

from osha.accidents import Accident, load_accidents
from osha.test.test_data.folder_structure import folder_structure


class TestAccidentDetailList(unittest.TestCase):

    def test_accidents_count(self):
        accidents = self._load_accidents('office-0100000-index-000000-detail.html')
        self.assertEqual(20, len(accidents))

    def test_accidents_count_bis(self):
        accidents = self._load_accidents('nine-boxes.html')
        self.assertEqual(9, len(accidents))
        b0 = accidents[0]
        self.assertEqual('Accident: 200770659 - Employee Killed When Pinned Between Forklift And Dock', b0.main_title)
        assertStringContains('Accident: 200770659 -- Report ID: 0134000 -- Event Date: 12/31/1999', b0.table_html)
        assertStringContains('<a href="establishment.inspection_detail?id=113544209" title="113544209">', b0.table_html)

        b8 = accidents[8]
        self.assertEqual('Accident: 201520707 - Employee Fractures Bones After Falling 25 Feet From Scaffold',
                         b8.main_title)
        assertStringContains('Accident: 201520707 -- Report ID: 0111500 -- Event Date: 12/16/1999', b8.table_html)

    def _load_accidents(self, html) -> List[Accident]:
        path = (folder_structure.detail_pages / html)
        return load_accidents(path.read_text())


def assertStringContains(substring, string):
    if substring not in string:
        raise Exception(f'substring `{substring}` was not found in ```{string}```')

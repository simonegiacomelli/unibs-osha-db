import unittest
from typing import List

from osha.accidents import Accident, load_accidents, InspectionLine
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

    def test_complex_box(self):
        accidents = self._load_accidents('complex-box.html')
        self.assertEqual(1, len(accidents))
        b = accidents[0]
        self.assertEqual('Accident: 14412233 - Employee Killed In Explosion Due To Chemical Release', b.main_title)
        self.assertEqual(2, len(b.inspections))
        i0 = b.inspections[0]
        i1 = b.inspections[1]
        self.assertEqual(('106614357', '08/25/1989', '2821',
                          'Phillips 66 Company,Houston Chemical Complex'), i0.tuple())
        self.assertEqual(('106614373', '08/25/1989', '1795',
                          'Midwest Metals Industries, Inc.'), i1.tuple())

        self.assertEqual(5, len(b.lines))
        l0, *lr = b.lines
        l0: InspectionLine
        lr: List[InspectionLine]
        self.assertEqual(('1', '106614357', '', '', 'Fatality', 'Burn/Scald(Heat)',
                          'Occupation not reported'), l0.tuple())
        for idx, ln in enumerate(lr):
            self.assertEqual(
                (str(idx + 2), '106614373', '', '', 'Hospitalized injury', 'Burn/Scald(Heat)',
                 'Occupation not reported'), ln.tuple())

    def _load_accidents(self, html) -> List[Accident]:
        path = (folder_structure.detail_pages / html)
        return load_accidents(path.read_text())


def assertStringContains(substring, string):
    if substring not in string:
        raise Exception(f'substring `{substring}` was not found in ```{string}```')

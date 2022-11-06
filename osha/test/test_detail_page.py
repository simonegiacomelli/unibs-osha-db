import unittest

from osha.detail_page import DetailData
from osha.test.test_data.folder_structure import folder_structure


class TestInstanceList(unittest.TestCase):

    def disable_test_box_count(self):
        target = self._target('office-0100000-index-000000-detail.html')
        self.assertEqual(20, len(target.boxes))

    def disable_test_box_count_bis(self):
        target = self._target('nine-boxes.html')
        self.assertEqual(9, len(target.boxes))
        b0 = target.boxes[0]
        self.assertEqual('Accident: 200770659 - Employee Killed When Pinned Between Forklift And Dock', b0.main_title)
        self.assertEqual('Accident: 200770659 -- Report ID: 0134000 -- Event Date: 12/31/1999', b0.sub_title)

        b8 = target.boxes[8]
        self.assertEqual('Accident: 201520707 - Employee Fractures Bones After Falling 25 Feet From Scaffold',
                         b8.main_title)
        self.assertEqual('Accident: 201520707 -- Report ID: 0111500 -- Event Date: 12/16/1999', b8.sub_title)

    def test_no_keywords(self):
        target = self._target('no-keywords.html')
        self.assertEqual(1, len(target.boxes))

    def test_complex_box(self):
        target = self._target('complex-box.html')
        self.assertEqual(1, len(target.boxes))
        b = target.boxes[0]
        self.assertEqual(2, len(b.inspections))

        i_expected = (
            ('106614357', '08/25/1989', '2821', 'Phillips 66 Company,Houston Chemical Complex'),
            ('106614373', '08/25/1989', '1795', 'Midwest Metals Industries, Inc.')
        )
        for idx, inspection in enumerate(b.inspections):
            e = i_expected[idx]
            self.assertEqual(e[0], inspection.id)
            self.assertEqual(e[1], inspection.open_date)
            self.assertEqual(e[2], inspection.sic)
            self.assertEqual(e[3], inspection.establishment_name)

        self.assertTrue(b.description.startswith('TWO CONTRACTOR '), b.description)
        self.assertTrue(b.description.endswith(' LINE CAME OFF.'), b.description)
        exp_keywords = 'flammable vapors, explosion, process safety, maintenance, flammable liquid, fire, construction, welding, lockout'
        self.assertEqual(exp_keywords, b.keywords)
        # self.assertEqual(5, len(b.employees))

    def _target(self, html) -> DetailData:
        path = (folder_structure.detail_pages / html)
        target = DetailData()
        target.load_from_html(path.read_text())

        return target

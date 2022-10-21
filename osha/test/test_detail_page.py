import unittest

from osha.detail_page import DetailPage
from osha.search_page import SearchPage
from osha.test.test_data.folder_structure import folder_structure
from scraper.page import Page


class TestInstanceList(unittest.TestCase):

    def test_box_count(self):
        self._verify_instance_count(20, 'office-0100000-index-000000-detail.html')

    def _verify_instance_count(self, expected_box_count, html):
        path = (folder_structure.detail_pages / html)
        target = DetailPage(page=Page(path))
        target.parse()
        self.assertEqual(len(target.boxes), expected_box_count)


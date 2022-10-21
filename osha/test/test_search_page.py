import unittest

from osha.search_page import SearchPage
from osha.test.test_data.folder_structure import folder_structure
from scraper.page import Page


class TestInstanceList(unittest.TestCase):

    def test_total_instances_count(self):
        self.verify_instance_count(2899, 'office-0100000-index-000000-list.html')
        self.verify_instance_count(2899, 'office-0100000-index-000020-list.html')

    def verify_instance_count(self, expected_instance_count, html):
        path = (folder_structure.list_pages / html)
        target = SearchPage(page=Page(path))
        target.load()
        self.assertEqual(target.instances_count, expected_instance_count)

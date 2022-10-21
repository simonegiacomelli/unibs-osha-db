import unittest

from osha.parser.instances_catalogue import InstanceCatalogue
from osha.parser.test.test_data.folder_structure import folder_structure


class TestInstanceList(unittest.TestCase):

    def test_total_instances_count(self):
        self.verify_instance_count(2899, 'office-0100000-index-000000-list.html')
        self.verify_instance_count(2899, 'office-0100000-index-000020-list.html')

    def verify_instance_count(self, expected_instance_count, html):
        body = (folder_structure.list_pages / html).read_text()
        target = InstanceCatalogue(body)
        self.assertEqual(target.instances_count, expected_instance_count)

import unittest

from osha.search_page import SearchData
from osha.test.test_data.folder_structure import folder_structure


class TestInstanceList(unittest.TestCase):

    def test_total_instances_count(self):
        self.verify_instance_count(2899, 'office-0100000-index-000000-list.html',
                                   ['148834.015', '146476.015', '144028.015', '144164.015', '143870.015', '143822.015',
                                    '143632.015', '143488.015', '143328.015', '143291.015', '143292.015', '143502.015',
                                    '143286.015', '143255.015', '143308.015', '143223.015', '144351.015', '143069.015',
                                    '147390.015', '143422.015']
                                   )
        self.verify_instance_count(2899, 'office-0100000-index-000020-list.html',
                                   ['143872.015', '144913.015', '146032.015', '142898.015', '142972.015', '142878.015',
                                    '144705.015', '142756.015', '144685.015', '142697.015', '142631.015', '143070.015',
                                    '142652.015', '144910.015', '142457.015', '147075.015', '144914.015', '142088.015',
                                    '142137.015', '143283.015'])

    def verify_instance_count(self, expected_instance_count, html, accident_detail_ids):
        path = (folder_structure.search_pages / html)
        target = SearchData()
        target.load_from_html(path.read_text())
        self.assertEqual(expected_instance_count, target.instances_count)
        self.assertEqual(accident_detail_ids, target.accident_detail_ids, )

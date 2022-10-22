from pathlib import Path
from typing import List

from osha.detail_box import DetailBox
from scraper.page import CachablePage


class DetailPage:
    def __init__(self, accident_detail_ids: List[str] = [], path: Path = None, page: CachablePage = None):
        self.boxes = []
        if page is None:
            args = map(lambda e: f'id={e}', accident_detail_ids)
            ids = '&'.join(args)
            url = f'https://www.osha.gov/pls/imis/accidentsearch.accident_detail?' + ids
            self.page = CachablePage(path, url)
        else:
            self.page = page

    def parse(self):
        self.page.load()
        print('')
        soup = self.page.beautifulsoup()
        elements = soup.find_all('table')
        self.boxes = []
        for e in elements:
            box = DetailBox(e)
            self.boxes.append(box)

from pathlib import Path
from typing import List

from pydantic import BaseModel

from cache.source import Source
from osha.detail_box import DetailBox
from scraper.page import CachablePage


class DetailData(BaseModel):
    accident_detail_ids: List[str]
    url: str = ''


class DetailPage(Source[DetailData]):
    def __init__(self, accident_detail_ids: List[str] = [], path: Path = None, page: CachablePage = None):
        super().__init__('name1', 'detail-page', DetailData)
        self.d = DetailData(
            accident_detail_ids=accident_detail_ids
        )
        self.boxes = []
        if page is None:
            args = map(lambda e: f'id={e}', accident_detail_ids)
            ids = '&'.join(args)
            url = f'https://www.osha.gov/pls/imis/accidentsearch.accident_detail?' + ids
            self.page = CachablePage(path, url)
            self.d.url = url
        else:
            self.page = page

    def data(self) -> DetailData:
        self.page.load()
        print('')
        soup = self.page.beautifulsoup()
        elements = soup.find_all('table')
        self.boxes = []
        for e in elements:
            box = DetailBox(e)
            self.boxes.append(box)
        return self.d

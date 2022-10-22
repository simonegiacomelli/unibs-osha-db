from typing import List

from pydantic import BaseModel

from cache.cache import Cache
from core.hashlib import md5sum_str
from core.log_helper import log
from osha.detail_box import DetailBox
from scraper.page import CachablePage, beautifulsoup


class DetailData(BaseModel):
    accident_detail_ids: List[str] = []
    boxes: List[DetailBox] = []
    url: str = ''

    def load_from_html(self, html):
        soup = beautifulsoup(html)
        elements = soup.find_all('table')
        self.boxes = []
        for e in elements:
            box = DetailBox()
            self.boxes.append(box)


class DetailPage:
    def __init__(self, accident_detail_ids: List[str], cache: Cache):
        self.data = DetailData(
            accident_detail_ids=accident_detail_ids
        )

        ids_hash = md5sum_str(','.join(accident_detail_ids))
        base = f'detail/detail-{ids_hash}'
        html_path = cache.path_for(f'{base}.html')
        self.json_file = cache.path_for(f'{base}.json')
        args = map(lambda e: f'id={e}', accident_detail_ids)
        ids = '&'.join(args)
        url = f'https://www.osha.gov/pls/imis/accidentsearch.accident_detail?' + ids
        self.page = CachablePage(html_path, url)
        self.data.url = url

    def get_data(self) -> DetailData:
        if not self.json_file.exists():
            self.page.load()
            self.data.load_from_html(self.page.body)
            self.json_file.serialize_json(self.data)
        else:
            log(f'Using cache {self.json_file.name}')
        self.data = self.json_file.deserialize_json(DetailData)
        return self.data

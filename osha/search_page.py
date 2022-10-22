from pathlib import Path
from typing import Optional, List

from bs4 import Tag
from pydantic import BaseModel

import lista_istanze_url
from cache.cache import Cache
from core.log_helper import log
from osha.detail_page import DetailPage
from scraper.page import CachablePage, beautifulsoup

self_folder = Path(__file__).parent


class SearchData(BaseModel):
    accident_index: int = 0
    page_size: int = 0
    instances_count: int = -1
    accident_detail_ids: List[str] = []
    results_text: str = 'na'
    url: str = ''

    def next_search_page(self) -> Optional['SearchPage']:
        following_index = self.accident_index + self.page_size
        if following_index >= self.instances_count:
            return None
        return SearchPage(following_index, self.page_size)

    def load_from_html(self, html: str):
        soup = beautifulsoup(html)
        self._fill_results_info(soup)
        elems = soup.find_all('input', {'name': 'id'})
        self.accident_detail_ids = []
        for e in elems:
            e: Tag
            accident_detail_id = e.attrs.get('value')
            self.accident_detail_ids.append(accident_detail_id)

    def _fill_results_info(self, soup):
        def results_filter(tag: Tag):
            return tag.name == 'div' and tag.get('class') == ['text-right'] and \
                   'Results' in tag.text

        h = soup.find(results_filter)
        if h is not None:
            self.results_text = h.text.strip()
            txt = self.results_text.split(' of ')[1]
            self.instances_count = int(txt)
        else:
            self.results_text = ''
            self.instances_count = -1


class SearchPage:
    def __init__(self, accident_index=0, page_size=20, page: CachablePage = None):
        self.data = SearchData(accident_index=accident_index, page_size=page_size)
        self.cache = Cache(self_folder.parent / 'data' / f'index-{self.data.accident_index:06}')
        self.json_file = self.cache.path_for('search_data.json')
        # from body
        if page is None:
            self.data.url = lista_istanze_url.lista_istanze_url(accident_index, page_size)
            self.page = CachablePage(self.cache.path_for('search.html'), self.data.url)
        else:
            self.page = page

    def get_data(self) -> SearchData:
        if not self.json_file.exists():
            self.page.load()
            self.data.load_from_html(self.page.body)
            self.json_file.serialize_json(self.data)
        else:
            log(f'Using cache {self.json_file.name}')
        self.data = self.json_file.deserialize_json(SearchData)
        return self.data

    def load_details(self) -> DetailPage:
        path = Path(str(self.page.path).removesuffix('-search.html') + '-detail.html')
        dp = DetailPage(self.data.accident_detail_ids, path)
        return dp

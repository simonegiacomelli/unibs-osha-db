from pathlib import Path
from typing import Optional, List

from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel

import lista_istanze_url
from cache.source import Source, T
from cache.source_cache import source_wrap
from osha.detail_page import DetailPage
from scraper.page import CachablePage

self_folder = Path(__file__).parent


class SearchData(BaseModel):
    office: str
    accident_index: int
    page_size: int
    instances_count: int = -1
    accident_detail_ids: List[str] = []
    results_text: str = 'na'
    url: str = ''

    def next_search_page(self) -> Optional['SearchPage']:
        following_index = self.accident_index + self.page_size
        if following_index >= self.instances_count:
            return None
        pagina = SearchPage(self.office, following_index, self.page_size)
        return pagina



class SearchPage(Source[SearchData]):
    def __init__(self, office: str = '', accident_index=0, page_size=20, page: CachablePage = None):
        super().__init__('name1', 'search-page', SearchData)
        self.d = SearchData(
            office=office,
            accident_index=accident_index,
            page_size=page_size
        )
        # from body
        if page is None:
            self.cache_prefix = self_folder.parent / 'data' / ('office' + self.d.office) \
                                / f'office-{self.d.office}-index-{self.d.accident_index:06}'
            self.d.url = lista_istanze_url.lista_istanze_url(office, accident_index, page_size)
            self.page = CachablePage(Path(f'{self.cache_prefix}-search.html'), self.d.url)
        else:
            self.page = page

    def data(self) -> Optional[SearchData]:
        self._parse()
        return self.d

    def _parse(self):
        self.page.load()
        soup = self.page.beautifulsoup()
        self._fill_results_info(soup)
        print(f"`{self.d.results_text}`")
        elems = soup.find_all('input', {'name': 'id'})
        self.d.accident_detail_ids = []
        for e in elems:
            e: Tag
            accident_detail_id = e.attrs.get('value')
            self.d.accident_detail_ids.append(accident_detail_id)

    def _fill_results_info(self, soup):
        def results_filter(tag: Tag):
            return tag.name == 'div' and tag.get('class') == ['text-right'] and \
                   'Results' in tag.text

        h = soup.find(results_filter)
        if h is not None:
            self.d.results_text = h.text.strip()
            txt = self.d.results_text.split(' of ')[1]
            self.d.instances_count = int(txt)
        else:
            self.d.results_text = ''
            self.d.instances_count = -1

    def load_details(self) -> DetailPage:
        path = Path(str(self.page.path).removesuffix('-search.html') + '-detail.html')
        dp = DetailPage(self.d.accident_detail_ids, path)
        return dp

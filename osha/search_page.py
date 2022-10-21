from pathlib import Path
from typing import Optional, List

from bs4 import BeautifulSoup, Tag

import lista_istanze_url
from osha.detail_page import DetailPage
from scraper.page import Page

self_folder = Path(__file__).parent


class SearchPage:
    def __init__(self, office: str = '', accident_index=0, page_size=20, page: Page = None):
        self.office = office
        self.accident_index = accident_index
        self.page_size = page_size
        # from body
        self.instances_count = -1
        self.accident_detail_ids: List[str] = []
        self.results_text = 'na'
        if page is None:
            office_folder = self_folder.parent / 'data' / ('office' + self.office)
            base_name = f'office-{self.office}-index-{self.accident_index:06}'
            path = office_folder / f'{base_name}-search.html'
            url = lista_istanze_url.lista_istanze_url(office, accident_index, page_size)
            self.page = Page(path, url)
        else:
            self.page = page

    def next(self) -> Optional['SearchPage']:
        following_index = self.accident_index + self.page_size
        if following_index >= self.instances_count:
            return None
        pagina = SearchPage(self.office, following_index, self.page_size)
        return pagina

    def parse(self):
        self.page.load()
        soup = self.page.beautifulsoup()
        self._fill_results_info(soup)
        print(f"`{self.results_text}`")
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

    def load_details(self) -> DetailPage:
        path = Path(str(self.page.path).removesuffix('-search.html') + '-detail.html')
        dp = DetailPage(self.accident_detail_ids, path)
        return dp

from pathlib import Path
from typing import Optional

import lista_istanze_url
from osha.parser.instances_catalogue import InstanceCatalogue
from scraper.page import Page

self_folder = Path(__file__).parent


class IstanzaPagina:
    def __init__(self, office, istanza_index=0, pagina_size=100):
        self.office = office
        self.istanza_index = istanza_index
        self.pagina_size = pagina_size

        self.office_folder = self_folder / 'data' / ('office' + self.office)
        self.base_name = f'office-{self.office}-index-{self.istanza_index:06}'
        self.accident_detail = self.office_folder / f'{self.base_name}-detail.html'
        url = lista_istanze_url.lista_istanze_url(office, istanza_index, pagina_size)
        accident_search = self.office_folder / f'{self.base_name}-search.html'
        self.search_page = Page(url, accident_search)
        self._catalogue_from_body()

    def __str__(self):
        return self.search_page.path.name

    def next(self) -> Optional['IstanzaPagina']:
        following_index = self.istanza_index + self.pagina_size
        if following_index >= self.catalogue.instances_count:
            return None
        pagina = IstanzaPagina(self.office, following_index, self.pagina_size)
        return pagina

    def exists(self) -> bool:
        return self.search_page.path.exists()

    def _catalogue_from_body(self):
        self.catalogue = InstanceCatalogue(self.search_page.body)

    def load(self):
        self.search_page.load()
        self._catalogue_from_body()
        print(f"`{self.catalogue.results_text}`")

from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup
import lista_istanze_url
from osha.parser.instances_catalogue import InstanceCatalogue
from url_helper import url_open

self_folder = Path(__file__).parent


class IstanzaPagina:
    def __init__(self, office, istanza_index=0, pagina_size=100):
        self.office = office
        self.istanza_index = istanza_index
        self.pagina_size = pagina_size
        self.url = lista_istanze_url.lista_istanze_url(office, istanza_index, pagina_size)
        self.status = 0
        self.body = ''

        self.office_folder = self_folder / 'data' / ('office' + self.office)
        self.base_name = f'office-{self.office}-index-{self.istanza_index:06}'
        self.office_page = self.office_folder / f'{self.base_name}-list.html'
        self.content_page = self.office_folder / f'{self.base_name}-content.html'
        self._catalogue_from_body()

    def __str__(self):
        return self.office_page.name

    def load_from_url(self):
        status, body = url_open(self.url)
        body = f'<!-- url: {self.url} -->\n' + body.lstrip()
        self.status = status
        self.body = body
        self._catalogue_from_body()

    def load_from_disk(self):
        self.status = 0
        self.body = self.office_page.read_text()
        self._catalogue_from_body()

    def next(self) -> Optional['IstanzaPagina']:
        following_index = self.istanza_index + self.pagina_size
        if following_index >= self.catalogue.instances_count:
            return None
        pagina = IstanzaPagina(self.office, following_index, self.pagina_size)
        return pagina


    def salva(self):
        self.office_folder.mkdir(exist_ok=True, parents=True)
        self.office_page.write_text(self.body)

    def exists(self) -> bool:
        return self.office_page.exists()

    def _catalogue_from_body(self):
        self.catalogue = InstanceCatalogue(self.body)

    def load(self):
        print('  ', end='')
        if not self.exists():
            print(f'pagina {self} segue caricamento... ', end='')
            self.load_from_url()
            self.salva()
        else:
            self.load_from_disk()
            print(f'pagina {self} gia'' presente ', end='')

        print(f"`{self.catalogue.results_text}`")


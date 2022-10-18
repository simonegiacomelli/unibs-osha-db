from pathlib import Path

import lista_istanze_url
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

    def __str__(self):
        return self.office_page.name

    def load(self):
        status, content = url_open(self.url)
        self.body = content
        self.status = status

    def next(self) -> 'IstanzaPagina':

        pagina = IstanzaPagina(self.office, self.istanza_index + self.pagina_size, self.pagina_size)
        return pagina

    def more_pages(self):
        return True

    def salva(self):
        self.office_folder.mkdir(exist_ok=True, parents=True)
        self.office_page.write_text(self.body.lstrip())

    def exists(self) -> bool:
        return self.office_page.exists()

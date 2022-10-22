import sys
from pathlib import Path

from bs4 import BeautifulSoup

from core.log_helper import log
from core.run_catching import run_catching
from url_helper import url_open


class CachablePage:
    def __init__(self, path: Path, url: str = ''):
        self.path = path
        self.url = url
        self.status = 0
        self.body = ''

    def load(self):
        print('  ', end='')
        p = self.path.name
        if not self.path.exists():
            print(f'pagina {p} segue caricamento... ', end='')
            self.load_from_url()
            self.salva()
        else:
            self.load_from_disk()
            print(f'pagina {p} gia'' presente ', end='')

    def load_from_url(self):
        def function():
            return url_open(self.url)

        def on_error(ex):
            log(f'url in process: `{self.url}`')
        res = run_catching(function, retry=sys.maxsize, on_error=on_error)
        status, body = res
        body = f'<!-- url: {self.url} -->\n' + body.lstrip()
        self.status = status
        self.body = body

    def load_from_disk(self):
        self.status = 0
        self.body = self.path.read_text()

    def salva(self):
        self.path.parent.mkdir(exist_ok=True, parents=True)
        self.path.write_text(self.body)

    def beautifulsoup(self) -> BeautifulSoup:
        bs = BeautifulSoup(self.body, 'html.parser')
        return bs

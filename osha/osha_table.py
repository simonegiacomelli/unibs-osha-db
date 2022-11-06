from typing import List, Tuple, Sequence, Optional, Dict

import bs4
from pydantic import BaseModel

from scraper.page import beautifulsoup


class Table(BaseModel):
    header: Tuple[str, ...] = ()
    rows: List[Tuple[str, ...]] = []


class TableRow:
    def __init__(self, tr: bs4.Tag):
        tds = list(tr.find_all('td'))
        ths = list(tr.find_all('th'))
        self.is_header = len(tds) == 0 and len(ths) > 0
        self.is_data = len(ths) == 0 and len(tds) > 0

        def trimmed_inner_html(tag: bs4.Tag) -> str:
            contents = tag.text
            return contents.strip()

        self.header = tuple(map(trimmed_inner_html, ths))
        self.data = tuple(map(trimmed_inner_html, tds))


class OshaTable(BaseModel):
    tables_dict: Dict[Tuple[str, ...], Table] = {}

    def load_from_html(self, html):
        self.tables_dict.clear()
        soup = beautifulsoup(html)
        tables = soup.find_all('table')
        if len(tables) != 1:
            raise ValueError(f'It was expected one html table in the following html ```{html}```')
        table = tables[0]

        trs: Sequence[bs4.Tag] = table.find_all('tr')
        no_header = Table()
        last_table = no_header
        for tr in trs:
            table_row = TableRow(tr)
            if table_row.is_header:
                last_table = self.content_tables_by_header(last_table.header)
                if last_table is None:
                    last_table = self._add_table(table_row.header)
            elif table_row.is_data:
                if len(table_row.data) == len(last_table.header):
                    last_table.rows.append(table_row.data)
                else:
                    pass

    def content_tables_by_header(self, header: Sequence[str]) -> Optional[Table]:
        h = tuple(header)
        t = self.tables_dict.get(h, None)
        return t

    def _add_table(self, header: Sequence[str]):
        t = Table()
        t.header = tuple(header)
        self.tables_dict[t.header] = t
        return t

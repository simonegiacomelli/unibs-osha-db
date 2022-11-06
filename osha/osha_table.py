from typing import List, Tuple, Sequence, Optional, Dict

import bs4
from pydantic import BaseModel

from scraper.page import beautifulsoup


class Link(BaseModel):
    href: str
    text: str


class Table(BaseModel):
    header: Tuple[str, ...] = ()
    rows: List[Tuple[str | Link, ...]] = []


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
        no_header = self._add_table(())
        current_table = no_header
        for tr in trs:
            table_row = TableRow(tr)
            if table_row.is_header:
                current_table = self.content_tables_by_header(table_row.header)
                if current_table is None:
                    current_table = self._add_table(table_row.header)
            elif table_row.is_data:
                if len(table_row.data) == len(current_table.header):
                    current_table.rows.append(table_row.data)
                else:
                    no_header.rows.append(table_row.data)
            else:
                raise Exception(f'row not recognized ```{tr.prettify()}```')

    def content_tables_by_header(self, header: Sequence[str]) -> Optional[Table]:
        h = tuple(header)
        t = self.tables_dict.get(h, None)
        return t

    def content_tables_by_header_partial(self, header: Sequence[str]) -> Optional[Table]:
        h = tuple(header)
        h_len = len(h)
        candidates: List[Table] = []
        for key, value in self.tables_dict.items():
            if len(key) >= h_len:
                if key[:h_len] == h:
                    candidates.append(value)
        if len(candidates) == 0:
            return None
        if len(candidates) > 1:
            raise Exception(f'Multiple tables are found with the same initial header `{h}`')
        return candidates[0]

    def _add_table(self, header: Sequence[str]):
        t = Table()
        t.header = tuple(header)
        self.tables_dict[t.header] = t
        return t

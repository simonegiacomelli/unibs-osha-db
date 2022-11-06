from typing import List

from pydantic import BaseModel

from osha.detail_box import DetailBox
from scraper.page import beautifulsoup


class ContentTable(BaseModel):
    fields: List[str] = []
    rows: List[List[str]] = []


class OshaTable(BaseModel):
    content_tables: List[ContentTable] = []

    def load_from_html(self, html):
        soup = beautifulsoup(html)
        tables = soup.find_all('table')
        titles = soup.find_all('p', class_='text-center')
        if len(tables) != len(titles):
            raise ValueError('mismatch in detail_page')

        self.boxes = []
        for idx, table in enumerate(tables):
            box = DetailBox()
            box.main_title = titles[idx].text.strip()
            box.load_from(table.find_all('tr'))

            self.boxes.append(box)

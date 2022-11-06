from typing import List

from scraper.page import beautifulsoup


class Accident:

    def __init__(self):
        self.main_title = ''
        self.table_html = ''


def load_accidents(html: str) -> List[Accident]:
    soup = beautifulsoup(html)
    tables = soup.find_all('table')
    titles = soup.find_all('p', class_='text-center')
    if len(tables) != len(titles):
        raise ValueError('mismatch in detail_page')

    accidents = []
    for idx, table in enumerate(tables):
        box = Accident()
        box.main_title = titles[idx].text.strip()
        box.table_html = table.prettify()
        accidents.append(box)
    return accidents

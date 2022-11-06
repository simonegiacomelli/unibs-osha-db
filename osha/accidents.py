from typing import List

from osha.osha_table import OshaTable
from scraper.page import beautifulsoup


class Inspection:

    def __init__(self):
        self.inspection_id = ''
        self.open_date = ''
        self.sic = ''
        self.establishment_name = ''

    def tuple(self):
        return self.inspection_id, self.open_date, self.sic, self.establishment_name


class Accident:

    def __init__(self):
        self.inspections: List[Inspection] = []
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
        accident = Accident()
        accident.main_title = titles[idx].text.strip()
        accident.table_html = table.prettify()
        ot = OshaTable()
        ot.load_from_html(accident.table_html)
        inspections_table = ot.content_tables_by_header(('Inspection', 'Open Date', 'SIC', 'Establishment Name'))
        if inspections_table is not None:
            for inspection_row in inspections_table.rows:
                inspection = Inspection()
                accident.inspections.append(inspection)
                inspection.inspection_id = inspection_row[0]
                inspection.open_date = inspection_row[1]
                inspection.sic = inspection_row[2]
                inspection.establishment_name = inspection_row[3]

        accidents.append(accident)
    return accidents

from typing import List

import bs4
from pydantic import BaseModel


class Inspection(BaseModel):
    id: str = ''
    open_date: str = ''
    sic: str = ''
    establishment_name: str = ''


class Employee(BaseModel):
    number: int = 0
    inspection_id: str = ''


def to_matrix(rows: bs4.ResultSet):
    matrix = []
    for row in rows:
        row: bs4.Tag
        mrow = []
        for c in row.children:
            if isinstance(c, bs4.NavigableString):
                pass
            else:
                mrow.append(c.text.strip())
        matrix.append(mrow)
    return matrix


def invalid(msg):
    raise ValueError(msg)


class DetailBox(BaseModel):
    main_title: str = ''
    sub_title: str = ''
    description: str = ''
    keywords: str = ''
    inspections: List[Inspection] = []
    employees: List[Employee] = []

    def load_from(self, rows: bs4.ResultSet):
        table = to_matrix(rows)
        self.consume_subtitle(table)
        self.consume_inspections(table)
        self.consume_description(table)
        self.consume_keywords(table)
        self.consume_employees(table)
        if len(table) != 0:
            invalid(f'Table has unexpected remaining rows `{table}`')

    def consume_inspections(self, table):
        while table[0][0] == 'Inspection':
            d = table[1]
            i = Inspection()
            i.id = d[0]
            i.open_date = d[1]
            i.sic = d[2]
            i.establishment_name = d[3]
            self.inspections.append(i)
            del table[0:2]  # remove consumed inspection rows

    def consume_employees(self, table):
        header = table[0]
        if header[0] != 'Employee #':
            invalid(f'Expected header but found `{",".join(header)}`')
        del table[0]
        expected_number = 1
        while len(table) > 0 and table[0][0] == str(expected_number):
            d = table[0]
            e = Employee()
            e.number = expected_number
            self.employees.append(e)
            del table[0]  # remove consumed employee
            expected_number += 1

    def consume_subtitle(self, table):
        self.sub_title = table[0][0]
        del table[0]

    def consume_description(self, table):
        row = table[0]
        if len(row) != 1:
            invalid(f'Description row with one column expected')
        self.description = row[0]
        del table[0]

    def consume_keywords(self, table):
        row = table[0]
        if len(row) != 1:
            invalid(f'Keyword row with one column expected, table: `{table}`')
        keywords = row[0]
        keywords_prefix = 'Keywords: \n'
        if not keywords.startswith(keywords_prefix):
            return

        self.keywords = keywords.removeprefix('Keywords: \n')
        del table[0]

from typing import List

from codici_office_const import codici_office


def estrai_codici_office() -> List[str]:
    result = []
    for option in codici_office.split('\n'):
        if option.strip() == '':
            continue
        value_end = option.removeprefix('<option value="')
        try:
            idx = value_end.index('"')
        except ValueError as e:
            continue
        value = value_end[:idx]
        result.append(value)
    return result


if __name__ == '__main__':
    for value in estrai_codici_office():
        print(value)

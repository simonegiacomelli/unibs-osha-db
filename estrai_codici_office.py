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
        value = value.strip()
        if value != '':
            result.append(value)
    return list(sorted(result))


if __name__ == '__main__':
    for idx, value in enumerate(estrai_codici_office()):
        print(f'idx={idx:3} {value}')

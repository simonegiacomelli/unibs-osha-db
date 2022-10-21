from estrai_codici_office import estrai_codici_office
from osha.search_page import SearchPage


# url = 'https://www.osha.gov/pls/imis/AccidentSearch.html'
# content = url_open(url)
def main():
    pagina_size = 20
    istanza_index = 0
    codici_office = estrai_codici_office()
    for office_index, office in enumerate(codici_office):
        print(f'Codice office {office} {office_index + 1}/{len(codici_office)}')
        pagina = SearchPage(office, istanza_index, pagina_size)
        while pagina is not None:
            pagina.load()
            pagina = pagina.next()


if __name__ == '__main__':
    main()

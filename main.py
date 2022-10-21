from estrai_codici_office import estrai_codici_office
from osha.search_page import SearchPage


# url = 'https://www.osha.gov/pls/imis/AccidentSearch.html'
# content = url_open(url)
def main():
    pagina_size = 20
    istanza_index = 0
    codici_office = estrai_codici_office()
    for office_index, office in enumerate(codici_office):
        office_ord = office_index + 1
        office_len = len(codici_office)
        pagina = SearchPage(office, istanza_index, pagina_size)
        while pagina is not None:
            print(f'{office_ord:3}/{office_len:03} ', end='')
            pagina.parse()
            pagina.load_details().parse()
            pagina = pagina.next()


if __name__ == '__main__':
    main()

from cache.source_cache import source_wrap
from core.log_helper import log
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
        search_page = SearchPage(office, istanza_index, pagina_size)
        while search_page is not None:
            log(f'{office_ord:3}/{office_len:03} ', end='')
            search_data = source_wrap(search_page, search_page.cache_prefix).data()
            # pagina.load_details().parse()
            search_page = search_data.next_search_page()


if __name__ == '__main__':
    main()

from cache.source_cache import source_wrap
from osha.search_page import SearchPage, SearchData


# url = 'https://www.osha.gov/pls/imis/AccidentSearch.html'
# content = url_open(url)
def main():
    pagina_size = 1000
    accident_index = 0

    search_page = SearchPage(accident_index, pagina_size)
    while search_page is not None:
        search_data: SearchData = source_wrap(search_page, search_page.cache_prefix).data()

        # if len(search_data.accident_detail_ids) > 0:
        #     spp = str(search_page.cache_prefix) + '-detail'
        #     detail_page = DetailPage(search_data.accident_detail_ids, Path(spp + '-page.html'))
        #     source_wrap(detail_page, Path(spp)).data()

        search_page = search_data.next_search_page()


if __name__ == '__main__':
    main()

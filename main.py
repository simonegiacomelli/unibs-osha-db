from estrai_codici_office import estrai_codici_office
from istanza_pagina import IstanzaPagina


# url = 'https://www.osha.gov/pls/imis/AccidentSearch.html'
# content = url_open(url)
def main():
    pagina_size = 200
    istanza_index = 0
    codici_office = estrai_codici_office()
    for office_index, office in enumerate(codici_office):
        print(f'Codice office {office} {office_index + 1}/{len(codici_office)}')
        pagina = IstanzaPagina(office, istanza_index, pagina_size)
        while pagina is not None:
            print('  ', end='')
            if not pagina.exists():
                print(f'pagina {pagina} segue caricamento... ', end='')
                pagina.load_from_url()
                pagina.salva()
            else:
                pagina.load_from_disk()
                print(f'pagina {pagina} gia'' presente ', end='')

            print(f"`{pagina.catalogue.results_text}`")
            pagina = pagina.next()


if __name__ == '__main__':
    main()

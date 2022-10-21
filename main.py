from estrai_codici_office import estrai_codici_office
from istanza_pagina import IstanzaPagina


# url = 'https://www.osha.gov/pls/imis/AccidentSearch.html'
# content = url_open(url)
def main():
    pagina_size = 200
    istanza_index = 0
    for office in estrai_codici_office():

        pagina = IstanzaPagina(office, istanza_index, pagina_size)
        while pagina is not None:
            if not pagina.exists():
                print(f'pagina {pagina} segue caricamento')
                pagina.load_from_url()
                pagina.salva()
                # pagina.salvaDatiIstanze()
            else:
                print(f'pagina {pagina} gia'' presente')

            pagina = pagina.next()


if __name__ == '__main__':
    main()

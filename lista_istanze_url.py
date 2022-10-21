url1 = 'https://www.osha.gov/pls/imis/AccidentSearch.search?p_logger=1&acc_description=&acc_Abstract=&acc_keyword=&sic=&naics=&Office=0100000&officetype=All&endmonth=10&endday=18&endyear=2002&startmonth=10&startday=18&startyear=2023&InspNr='
url2 = 'https://www.osha.gov/pls/imis/AccidentSearch.search?p_logger=1&acc_description=&acc_Abstract=&acc_keyword=&sic=&naics=&Office=0200000&officetype=All&endmonth=10&endday=18&endyear=2002&startmonth=10&startday=18&startyear=2023&InspNr='
url3 = 'https://www.osha.gov/pls/imis/accidentsearch.search?sic=&sicgroup=&naics=&acc_description=&acc_abstract=&acc_keyword=&inspnr=&fatal=&officetype=All&office=0200000&startmonth=10&startday=18&startyear=2023&endmonth=10&endday=18&endyear=2002&keyword_list=&p_start=&p_finish=20&p_sort=&p_desc=DESC&p_direction=Next&p_show=20'
url4 = 'https://www.osha.gov/pls/imis/accidentsearch.search?sic=&sicgroup=&naics=&acc_description=&acc_abstract=&acc_keyword=&inspnr=&fatal=&officetype=All&office=0200000&startmonth=10&startday=18&startyear=2023&endmonth=10&endday=18&endyear=2002&keyword_list=&p_start=&p_finish=40&p_sort=&p_desc=DESC&p_direction=Next&p_show=20'

url_con_multi_incident = 'https://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=143273.015&id=144429.015&id=143288.015&id=143306.015&id=142862.015&id=142399.015&id=143554.015&id=145866.015&id=140158.015&id=140943.015&id=139577.015&id=136393.015&id=136124.015&id=134968.015&id=131545.015&id=130579.015&id=128609.015&id=127680.015&id=125488.015&id=124207.015&id=121963.015'
url_con_multi_inspection_multi_incident = 'https://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14412233'
url_con_colonna_aggiuntiva = 'https://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=127680.015'

url_view = 'https://www.osha.gov/pls/imis/accidentsearch.search?' \
           'sic=' \
           '&sicgroup=' \
           '&naics=' \
           '&acc_description=' \
           '&acc_abstract=' \
           '&acc_keyword=' \
           '&inspnr=' \
           '&fatal=' \
           '&officetype=All' \
           '&office=0200000' \
           '&startmonth=10' \
           '&startday=18' \
           '&startyear=2023' \
           '&endmonth=10' \
           '&endday=18' \
           '&endyear=2002' \
           '&keyword_list=' \
           '&p_start=' \
           '&p_finish=40' \
           '&p_sort=' \
           '&p_desc=DESC' \
           '&p_direction=Next' \
           '&p_show=20'


def lista_istanze_url(office: str, istanza_index: int, pagina_size: int) -> str:
    url_template = 'https://www.osha.gov/pls/imis/accidentsearch.search?' \
                   'sic=' \
                   '&sicgroup=' \
                   '&naics=' \
                   '&acc_description=' \
                   '&acc_abstract=' \
                   '&acc_keyword=' \
                   '&inspnr=' \
                   '&fatal=' \
                   '&officetype=All' \
                   f'&office={office}' \
                   '&startmonth=12' \
                   '&startday=31' \
                   '&startyear=2099' \
                   '&endmonth=1' \
                   '&endday=1' \
                   '&endyear=1984' \
                   '&keyword_list=' \
                   '&p_start=' \
                   f'&p_finish={istanza_index}' \
                   '&p_sort=' \
                   '&p_desc=ASC' \
                   '&p_direction=Next' \
                   f'&p_show={pagina_size}'
    return url_template

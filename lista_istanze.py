url1 = 'https://www.osha.gov/pls/imis/AccidentSearch.search?p_logger=1&acc_description=&acc_Abstract=&acc_keyword=&sic=&naics=&Office=0100000&officetype=All&endmonth=10&endday=18&endyear=2002&startmonth=10&startday=18&startyear=2023&InspNr='
url2 = 'https://www.osha.gov/pls/imis/AccidentSearch.search?p_logger=1&acc_description=&acc_Abstract=&acc_keyword=&sic=&naics=&Office=0200000&officetype=All&endmonth=10&endday=18&endyear=2002&startmonth=10&startday=18&startyear=2023&InspNr='
url3 = 'https://www.osha.gov/pls/imis/accidentsearch.search?sic=&sicgroup=&naics=&acc_description=&acc_abstract=&acc_keyword=&inspnr=&fatal=&officetype=All&office=0200000&startmonth=10&startday=18&startyear=2023&endmonth=10&endday=18&endyear=2002&keyword_list=&p_start=&p_finish=20&p_sort=&p_desc=DESC&p_direction=Next&p_show=20'
url4 = 'https://www.osha.gov/pls/imis/accidentsearch.search?sic=&sicgroup=&naics=&acc_description=&acc_abstract=&acc_keyword=&inspnr=&fatal=&officetype=All&office=0200000&startmonth=10&startday=18&startyear=2023&endmonth=10&endday=18&endyear=2002&keyword_list=&p_start=&p_finish=40&p_sort=&p_desc=DESC&p_direction=Next&p_show=20'

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


def url_template(office: str) -> str:
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
    return url_template

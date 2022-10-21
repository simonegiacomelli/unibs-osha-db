from bs4 import BeautifulSoup, Tag


class InstanceCatalogue:
    def __init__(self, body: str):
        self.body = body
        self.instances_count = -1
        self._body_changed()

    def _body_changed(self):
        soup = BeautifulSoup(self.body, 'html.parser')

        # search = [f.find_all('div', class_='text-right') for f in soup.find_all('div', class_="span3")]
        def filter(tag: Tag):
            return tag.name == 'div' and tag.get('class') == ['text-right'] and \
                   'Results' in tag.text

        h = soup.find(filter)
        if h is not None:
            txt = h.text.split(' of ')[1]
            self.instances_count = int(txt)
        else:
            self.instances_count = -1

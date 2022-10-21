from bs4 import BeautifulSoup, Tag


class InstanceCatalogue:
    def __init__(self, body: str):
        self.body = body
        self.instances_count = -1
        self.results_text = 'na'
        self._body_changed()

    def _body_changed(self):
        soup = BeautifulSoup(self.body, 'html.parser')

        def results_filter(tag: Tag):
            return tag.name == 'div' and tag.get('class') == ['text-right'] and \
                   'Results' in tag.text

        h = soup.find(results_filter)
        if h is not None:
            self.results_text = h.text.strip()
            txt = self.results_text.split(' of ')[1]
            self.instances_count = int(txt)
        else:
            self.results_text = ''
            self.instances_count = -1

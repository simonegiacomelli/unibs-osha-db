from pathlib import Path

parent = Path(__file__).parent


class FolderStructure:
    def __init__(self):
        self.test_data = parent
        self.search_pages = self.test_data / 'search_pages'
        self.detail_pages = self.test_data / 'detail_pages'


folder_structure = FolderStructure()

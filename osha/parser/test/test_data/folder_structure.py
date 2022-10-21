from pathlib import Path

parent = Path(__file__).parent


class FolderStructure:
    def __init__(self):
        self.test_data = parent
        self.list_pages = self.test_data / 'list_pages'


folder_structure = FolderStructure()

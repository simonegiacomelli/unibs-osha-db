from pathlib import Path
from typing import List

from cardiospire_uds.uds.uds import UDS
from cardiospire_uds.uds.uds_feed import UDS_Feed


class Mock_UDS(UDS):
    def __init__(self, src: str, has_error: bool = False):
        self.src = Path(src)
        super().__init__(self.src.name, 'MOCK')
        if has_error:
            self.errors.append('mock error')

class Mock_UDS_Feed(UDS_Feed):

    def __init__(self, mock_items: List[UDS]):
        super().__init__()
        self.mock_items = mock_items

    def load_items(self):
        self.items.extend(self.mock_items)

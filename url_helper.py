import urllib.request
from typing import Tuple


def url_open(url, encodings=('utf-8', 'ascii', 'windows-1252', 'windows-1250')) -> Tuple[int, str]:
    response = urllib.request.urlopen(url)
    s = response.read()
    for encoding in encodings:
        try:
            content = s.decode(encoding)
            return response.status, content
        except UnicodeDecodeError:
            pass

    raise Exception(f'unable to decode content')

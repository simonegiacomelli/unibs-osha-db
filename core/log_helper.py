from datetime import datetime


def log(msg, end=None):
    n = datetime.now()
    print(f'{n:%Y-%m-%d %H:%M:%S} {msg}', flush=True, end=end)

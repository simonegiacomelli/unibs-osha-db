from hashlib import md5


def md5sum(filename):
    h = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * h.block_size), b""):
            h.update(chunk)
    return h.hexdigest()

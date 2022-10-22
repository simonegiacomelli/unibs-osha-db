from pathlib import Path
from typing import List


def read_lines(path: Path, at_most: int) -> List[str]:
    lines = []
    with open(path) as f:
        try:
            for i in range(at_most):
                lines.append(next(f))
        except StopIteration:
            pass
    return lines

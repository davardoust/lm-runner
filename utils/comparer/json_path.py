from collections.abc import Mapping, Sequence
from typing import Any, List


class JSONPathExtractor:
    @staticmethod
    def get(obj: Any, path: str) -> List[Any]:
        parts = path.replace("[", ".[").split(".")
        current = [obj]

        for part in parts:
            if not part:
                continue

            if part.startswith("["):
                idx = int(part[1:-1])
                current = [
                    c[idx]
                    for c in current
                    if isinstance(c, Sequence) and not isinstance(c, (str, bytes))
                    and 0 <= idx < len(c)
                ]
            else:
                current = [
                    c[part]
                    for c in current
                    if isinstance(c, Mapping) and part in c
                ]

        return current

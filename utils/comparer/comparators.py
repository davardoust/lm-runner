from typing import Any, Dict, List, Optional
from .json_path import JSONPathExtractor
from .scorers import ValueScorer


class PartialJSONComparator:
    def compare(
        self,
        json1: Any,
        json2: Any,
        paths: List[str],
        list_key_map: Optional[Dict[str, str]] = None,
    ) -> float:

        list_key_map = list_key_map or {}
        total, max_total = 0.0, 0.0

        for path in paths:
            vals1 = JSONPathExtractor.get(json1, path)
            vals2 = JSONPathExtractor.get(json2, path)

            n = min(len(vals1), len(vals2))
            for i in range(n):
                sc, mx = ValueScorer.score(vals1[i], vals2[i])
                total += sc
                max_total += mx

            max_total += abs(len(vals1) - len(vals2))

        return round((total / max_total) * 100, 2) if max_total else -1

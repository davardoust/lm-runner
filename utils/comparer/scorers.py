from typing import Any, Tuple
from utils.util import *


class ValueScorer:
    @staticmethod
    def score(v1: Any, v2: Any) -> Tuple[float, float]:
        v1, v2 = normalize_value(v1), normalize_value(v2)

        if isinstance(v1, (int, float)) or isinstance(v2, (int, float)):
            return ValueScorer._score_numeric(v1, v2)

        if isinstance(v1, str) and isinstance(v2, str):
            return string_similarity(v1, v2), 1.0

        return 0.0, 1.0

    @staticmethod
    def _score_numeric(v1, v2) -> Tuple[float, float]:
        n1, n2 = to_numeric(v1), to_numeric(v2)
        return (1.0, 1.0) if n1 == n2 else (0.0, 1.0)

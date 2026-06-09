import numpy as np
from typing import List, Dict
from utils.util import string_similarity


class TestAligner:
    def align(
        self,
        label_tests: List[Dict],
        predicted_tests: List[Dict],
    ) -> List[tuple[int, int]]:
        
        matches = []
        used_predictions = set()
        
        for i, label in enumerate(label_tests):
            best_score = -1
            best_pred_idx = -1
            
            for j, pred in enumerate(predicted_tests):
                score = string_similarity(label["test_name"], pred.get("test_name", ""))
                if score > best_score and j not in used_predictions:
                    best_score = score
                    best_pred_idx = j
            
            if best_pred_idx != -1:
                matches.append((i, best_pred_idx))
                used_predictions.add(best_pred_idx)
        
        return matches

from typing import List, Dict
from .alignment import TestAligner
from .comparators import PartialJSONComparator


class LabReportEvaluator:
    def __init__(self, paths: List[str]):
        self.paths = paths
        self.aligner = TestAligner()
        self.comparator = PartialJSONComparator()

    def evaluate(
        self,
        label_tests: List[Dict],
        predicted_tests: List[Dict],
        predicted_tests_has_score: bool = True
    ) -> Dict:

        if predicted_tests_has_score:
            predicted_tests = flatten_ocr_results(predicted_tests)


        matches = self.aligner.align(label_tests, predicted_tests)
        total_score = 0.0

        for li, pi in matches:
            score = self.comparator.compare(
                label_tests[li],
                predicted_tests[pi],
                self.paths,
            )
            predicted_tests[pi]["score"] = score
            total_score += score

        return {
            "avg_score": total_score / len(label_tests),
            "items": predicted_tests,
        }



def flatten_ocr_results(ocr_data):
    return [
        {key: value['text'] if isinstance(value, dict) and 'text' in value else value 
         for key, value in item.items()}
        for item in ocr_data
    ]
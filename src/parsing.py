import json
from schemas import LabReport
from pydantic import ValidationError

class OutputParser:
    def __init__(self, logger):
        self.logger = logger

    def parse_and_validate(self, raw_json_str: str) -> dict:
        """
        Attempts to parse string to JSON, then validates via Pydantic.
        """
        try:
            # 1. Parse JSON string
            data = json.loads(raw_json_str)
            
            # 2. Pydantic Validation
            # This fills in defaults and checks types
            validated_data = LabReport(**data)
            
            # 3. Return dict
            return validated_data.model_dump()
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON Parsing Error: {e}")
            self.logger.debug(f"Bad JSON Content: {raw_json_str[:100]}...")
            raise e
        except ValidationError as e:
            self.logger.error(f"Schema Validation Error: {e}")
            # We return the raw data if schema fails, but marked as invalid in pipeline
            return {"error": "Validation Failed", "details": str(e), "raw": data}

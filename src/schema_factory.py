from typing import Type

from pydantic import BaseModel

class SchemaFactory:
    @staticmethod
    def get_schema(schema_name: str) -> Type[BaseModel]:
        try:
            if schema_name == "LabReport":
                from schemas import LabReport
                return LabReport
            # elif schema_name == "MedicalDiagnosis":
            #     from schemas import MedicalDiagnosis
            #     return MedicalDiagnosis
            else:
                return None
        except ImportError as e:
            # Log and return None or raise a custom exception
            return None
     
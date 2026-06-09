from typing import Type

from pydantic import BaseModel

class SchemaFactory:
    @staticmethod
    def get_schema(schema_name: str) -> Type[BaseModel]:
        try:
            if schema_name == "LabReport":
                from src.schemas import LabReportSchema
                return LabReportSchema
            
            if schema_name == "TestSection":
                from src.schemas import TestSectionSchema
                return TestSectionSchema
            
            # elif schema_name == "MedicalDiagnosis":
            #     from schemas import MedicalDiagnosis
            #     return MedicalDiagnosis
            else:
                return None
        except ImportError as e:
            # Log and return None or raise a custom exception
            return None
     
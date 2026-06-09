from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field

class PatientInfoSchema(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    national_code: Optional[str] = None

class LabInfoSchema(BaseModel):
    name: Optional[str] = None
    code: Optional[Union[int, str]] = None
    technical_officer: Optional[str] = None

class DoctorInfoSchema(BaseModel):
    name: Optional[str] = None

class Header(BaseModel):
    patient_info: PatientInfoSchema = Field(default_factory=PatientInfoSchema)
    lab_info: LabInfoSchema = Field(default_factory=LabInfoSchema)
    doctor_info: DoctorInfoSchema = Field(default_factory=DoctorInfoSchema)
    date: Optional[str] = None
    receipt_no: Optional[Union[int, str]] = None
    test_no: Optional[str] = None
    answer_date: Optional[str] = None

class TestItemSchema(BaseModel):
    test_name: str
    result: Union[float, str, None]
    unit: Optional[str] = None
    reference_value: Optional[str] = None
    method: Optional[str] = None
    note: Optional[str] = None

class TestSectionSchema(BaseModel):   
    section: str
    tests: List[TestItemSchema] = []

class LabReportSchema(BaseModel):
    header: Header = Field(default_factory=Header)
    tests: List[TestSectionSchema] = []


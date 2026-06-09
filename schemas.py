from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field

class PatientInfo(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    national_code: Optional[str] = None

class LabInfo(BaseModel):
    name: Optional[str] = None
    code: Optional[Union[int, str]] = None
    technical_officer: Optional[str] = None

class DoctorInfo(BaseModel):
    name: Optional[str] = None

class Header(BaseModel):
    patient_info: PatientInfo = Field(default_factory=PatientInfo)
    lab_info: LabInfo = Field(default_factory=LabInfo)
    doctor_info: DoctorInfo = Field(default_factory=DoctorInfo)
    date: Optional[str] = None
    receipt_no: Optional[Union[int, str]] = None
    test_no: Optional[str] = None
    answer_date: Optional[str] = None

class TestItem(BaseModel):
    test_name: str
    result: Union[float, str, None]
    unit: Optional[str] = None
    reference_value: Optional[str] = None
    method: Optional[str] = None
    note: Optional[str] = None

class TestSection(BaseModel):   
    section: str
    tests: List[TestItem] = []

class LabReport(BaseModel):
    header: Header = Field(default_factory=Header)
    tests: List[TestSection] = []

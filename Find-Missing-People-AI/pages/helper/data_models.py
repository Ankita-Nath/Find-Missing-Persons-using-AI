from dataclasses import dataclass
from typing import Optional


@dataclass
class NewCaseDetails:
    id: str
    name: str
    fathers_name: Optional[str]
    age: int
    mobile_number: str
    description: Optional[str]
    face_embedding: list
    submitted_by: str
    birth_marks: Optional[str]
    adhaar_card: str
    address: str
    last_seen: str
    complainant_name: str
    complainant_mobile: str


@dataclass
class UserSubmission:
    name: str
    address: str
    face_encoding: list
    id: str
    mobile: int
    birth_marks: Optional[str] = None

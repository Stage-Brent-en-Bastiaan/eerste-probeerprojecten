from typing import Any
from dataclasses import dataclass
import json
from typing import List
from typing import Any
from dataclasses import dataclass
import json


@dataclass
class Patient:
    id: int
    # box_code: str
    first_name: str
    last_name: str
    # phone_contact: str
    # phone_auth: str
    # gov_id: str
    # hospital_id: str
    date_of_birth: str
    gender: str
    # address: str
    nationality: str
    # locale: str

    @staticmethod
    def fromBewellApiModel(patient):
        newPatient = Patient(
            id=patient.id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth,
            gender=patient.gender,
            nationality=patient.nationality,
        )
        return newPatient

    def toDict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "nationality": self.nationality,
        }

from typing import Optional, List
from pydantic import BaseModel
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from beanie import Document

PyObjectId = Annotated[str, BeforeValidator(str)]


class CompanyName(BaseModel):
    primary: Optional[str]
    secondary: Optional[str]
    tertiary: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "primary": "asdsad",
                "secondary": "dasda",
                "tertiary": "asdasd",
            }
        }


class Address(BaseModel):
    street: Optional[str]
    postalCode: Optional[str]
    city: Optional[str]
    postFach: Optional[str]
    plzPostfach: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "street": "",
                "postalCode": 0,
                "city": "",
                "postFach": 0,
                "plzPostfach": 0,
            }
        }


class Salutation(BaseModel):
    anrede: Optional[str]
    title: Optional[str]
    anredezeile: Optional[str]

    class Config:
        json_schema_extra = {
            "anrede": "",
            "title": "",
            "anredezeile": "",
        }


class Person(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    abteilungszusatz: Optional[str]

    class Config:
        json_schema_extra = {
            "firstName": "",
            "lastName": "",
            "abteilungszusatz": "",
        }


class PhoneNumber(BaseModel):
    vorwahl: Optional[str]
    number: Optional[str]

    class Config:
        json_schema_extra = {
            "vorwahl": 0,
            "number": 0,
        }


class Contact(BaseModel):
    salutation: Salutation
    person: Person
    phoneNumber: PhoneNumber
    faxNumber: Optional[str]
    email: Optional[str]
    website: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "street": "",
                "postalCode": 0,
                "city": "",
                "postFach": 0,
                "plzPostfach": 0,
            }
        }


class Location(BaseModel):
    bundesland: Optional[str]
    regierungsbezirk: Optional[str]
    kreis: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "bundesland": "",
                "regierungsbezirk": "",
                "kreis": "",
            }
        }


class Company(Document):
    _id: Optional[PyObjectId]
    companyNames: CompanyName
    address: Address
    contact: Contact
    location: Location
    employmentSize: Optional[str]
    branchCodes: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "_id": {"$oid": "680282195a4c5159edcbcf2d"},
                "companyNames": {
                    "primary": "12 Inch Records e.K.",
                    "secondary": "asdasd",
                    "tertiary": "asdad",
                },
                "address": {
                    "street": "Verlängerte Werderstr 40",
                    "postalCode": 12524,
                    "city": "Berlin",
                    "postFach": 67,
                    "plzPostfach": 45646,
                },
                "contact": {
                    "salutation": {
                        "anrede": "asdad",
                        "title": "asdsada",
                        "anredezeile": "Sehr geehrte Damen und Herren",
                    },
                    "person": {
                        "firstName": "asdsad",
                        "lastName": "adasds",
                        "function": "asdsad",
                        "abteilungszusatz": "asdada",
                    },
                    "phoneNumber": {
                        "vorwahl": 30,
                        "number": 67898362,
                    },
                    "faxNumber": 1231313,
                    "email": "kontakt@12inch-records.de",
                    "website": "www.12inch-records.de",
                },
                "location": {
                    "bundesland": "Berlin",
                    "regierungsbezirk": "asdasdasd",
                    "kreis": "Berlin, Stadt",
                },
                "employmentSize": "bis 5",
                "branchCodes": [
                    "Tonträger Einzelhandel",
                ],
            }
        }

    class Settings:
        name = "companies"

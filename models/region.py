from typing import Optional, List
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from beanie import Document

PyObjectId = Annotated[str, BeforeValidator(str)]


class Region(Document):
    _id: Optional[PyObjectId]
    region: str

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "680296d2d477dfb670daf94a",
                "region": "Medical",
            }
        }

    class Settings:
        name = "regions"
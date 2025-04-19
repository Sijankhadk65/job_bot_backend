from typing import Optional
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from beanie import Document

PyObjectId = Annotated[str, BeforeValidator(str)]


class Category(Document):
    _id: Optional[PyObjectId]
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "680296d2d477dfb670daf94a",
                "name": "Medical Equipment Manufacturing",
            }
        }

    class Settings:
        name = "category"

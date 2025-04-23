from typing import Optional
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from beanie import Document

PyObjectId = Annotated[str, BeforeValidator(str)]


class Code(Document):
    _id: Optional[PyObjectId]
    code: str

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "680296d2d477dfb670daf94a",
                "code": "Medical Equipment Manufacturing",
            }
        }

    class Settings:
        name = "codes"

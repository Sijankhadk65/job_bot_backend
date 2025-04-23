from fastapi import APIRouter
from models.response import Response
from database.database import *

router = APIRouter()


@router.get(
    "/",
    response_description="List of all the codes",
    response_model=Response,
)
async def get_codes():
    codes = await retrive_codes()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "codes",
        "data": codes,
    }

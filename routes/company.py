from fastapi import APIRouter
from models.response import Response
from database.database import *

router = APIRouter()


@router.get(
    "/",
    response_description="List of all the companies",
    response_model=Response,
)
async def get_companies():
    companies = await retrive_companies()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Companies",
        "data": companies,
    }


@router.get(
    "/filters",
    response_description="List of all the companies of a specific city",
    response_model=Response,
)
async def get_companies():
    companies = await retrive_select_companies()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Companies",
        "data": companies,
    }

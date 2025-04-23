from typing import List
from models.code import Code
from models.company import Company
from models.category import Category

code_collection = Code
company_collection = Company
category_collection = Category


async def retrive_codes() -> List[Code]:
    codes = await code_collection.all().to_list()
    return codes

async def retrive_categories() -> List[Category]:
    categories = await category_collection.all().to_list()
    return categories

async def retrive_category_codes(category: str) -> List[Code]:
    categorized_codes: Category = await category_collection.find(Category.category == category).first_or_none()
    return categorized_codes.codes


async def retrive_companies() -> List[Company]:
    companies = await company_collection.all().to_list()
    return companies


async def retrive_coded_companies(filters) -> List[Company]:
    companies = await company_collection.find(
        filters
    ).to_list()
    return companies

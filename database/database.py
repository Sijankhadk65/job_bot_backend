from typing import List
from models.category import Category
from models.company import Company

category_collection = Category
company_collection = Company


async def retrive_categories() -> List[Category]:
    categories = await category_collection.all().to_list()
    return categories


async def retrive_companies() -> List[Company]:
    companies = await company_collection.all().to_list()
    return companies


async def retrive_select_companies(filters) -> List[Company]:
    companies = await company_collection.find(
        Company.address.city == "Berlin"
    ).to_list()
    return companies

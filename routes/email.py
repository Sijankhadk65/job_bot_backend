import os
from uuid import uuid4
import shutil
from fastapi import APIRouter
from tasks import send_bulk_email_task, test_task
from dotenv import load_dotenv
from database.database import *
from beanie.operators import In, And
from fastapi import (
    Request,
    HTTPException,
    status,
    Depends,
    Form,
    UploadFile,
    File,
)

load_dotenv()

router = APIRouter()

SECRET_TOKEN = os.getenv("AUTH_TOKEN")


def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = auth_header.split("Bearer ")[1]
    if token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )


@router.get("/test_emails")
async def test_emails():
    test_task.delay("Sijan")


@router.post("/")
async def trigger_bulk_email(
    _: None = Depends(verify_token),
    email: str = Form(...),
    password: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    categories: List[str] = Form(None),
    attachments: List[UploadFile] = File(None),
):
    # Save uploaded files to a temp folder
    temp_dir = f"temp_uploads/{uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)

    print("Sending emails...")
    print(f"The send is: {email}")

    filters = []

    def save_upload(file: UploadFile, name: str) -> str:
        file_path = f"{temp_dir}/{name}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    try:        
        attachment_paths = []
        for attachment in attachments:
           attachment_paths.append(save_upload(attachment,attachment.filename))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    
    codes = []
    
    print("🕚 Fetching Categorized Codes from Database...")
    for category in categories:
        category_codes = await retrive_category_codes(category)
        codes.extend(category_codes)

    print("🕚 Fetching Companies from Database...")
    companies = await retrive_coded_companies(In("branchCodes", codes))
    print(f"✅ Email Data Fetched: {len(companies)} Fetched")
    companies_dict_list = [c.model_dump(exclude={"id", "_id"}) for c in companies]

    result = send_bulk_email_task.delay(
        sender=email,
        password=password,
        subject=subject,
        body=body,
        attachment_paths=attachment_paths,
        companies=companies_dict_list,
    )
    
    return {"message": "Router reached"}

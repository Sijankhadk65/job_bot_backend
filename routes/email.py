import os
from uuid import uuid4
import shutil
from fastapi import APIRouter
from tasks import send_bulk_email_task
from dotenv import load_dotenv
from database.database import *
from fastapi import (
    FastAPI,
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


@router.post("/")
async def trigger_bulk_email(
    _: None = Depends(verify_token),
    email: str = Form(...),
    password: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    cv: UploadFile = File(...),
    reference_letter: UploadFile = File(...),
):
    # Save uploaded files to a temp folder
    temp_dir = f"temp_uploads/{uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)

    def save_upload(file: UploadFile, name: str) -> str:
        file_path = f"{temp_dir}/{name}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    try:
        cv_path = save_upload(cv, "cv.pdf")
        ref_path = save_upload(reference_letter, "reference_letter.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    print("🕚 Fetching Emails from Database...")
    companies = await retrive_companies()
    print(f"✅ Email Data Fetched: {len(companies)} Fetched")
    companies_dict_list = [c.model_dump(exclude={"id", "_id"}) for c in companies]

    result = send_bulk_email_task.delay(
        sender=email,
        password=password,
        subject=subject,
        body=body,
        attachment_paths=[cv_path, ref_path],
        companies=companies_dict_list,
    )
    return {"message": "Bulk email process completed", "results": result.id}

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
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import shutil
from uuid import uuid4
from tasks import test_task

load_dotenv()

app = FastAPI()

# Allow all origins (for development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/")
def root():
    return {"status": "Server is up"}


@app.get("/test_celery/{name}")
async def test_celery_tasks(name: str):
    task = test_task.delay(name)
    return {"message": "task was invoked", "results": task.id}


# @app.post("/send-mails")
# async def trigger_bulk_email(
#     _: None = Depends(verify_token),
#     email: str = Form(...),
#     password: str = Form(...),
#     subject: str = Form(...),
#     body: str = Form(...),
#     cv: UploadFile = File(...),
#     reference_letter: UploadFile = File(...),
# ):
#     # Save uploaded files to a temp folder
#     temp_dir = f"temp_uploads/{uuid4()}"
#     os.makedirs(temp_dir, exist_ok=True)

#     def save_upload(file: UploadFile, name: str) -> str:
#         file_path = f"{temp_dir}/{name}"
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
#         return file_path

#     try:
#         cv_path = save_upload(cv, "cv.pdf")
#         ref_path = save_upload(reference_letter, "reference_letter.pdf")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

#     result = send_bulk_email_task.delay(
#         sender=email,
#         password=password,
#         subject=subject,
#         body=body,
#         attachment_paths=[cv_path, ref_path],
#     )
#     return {"message": "Bulk email process completed", "results": result.id}

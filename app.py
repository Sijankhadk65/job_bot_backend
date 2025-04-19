from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import initiate_database

from routes.catergory import router as CategoryRouter
from routes.email import router as EmailRouter
from routes.company import router as CompanyRouter

app = FastAPI()

# Allow all origins (for development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Roots"])
def root():
    return {"status": "Server is up"}


app.include_router(CategoryRouter, tags=["Category"], prefix="/categories")
app.include_router(CompanyRouter, tags=["Company"], prefix="/companies")
app.include_router(EmailRouter, tags=["Email"], prefix="/send_emails")

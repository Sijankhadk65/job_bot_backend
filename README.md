
# 📬 Job Bot Backend (Python : FastAPI + Celery)

A backend service to send bulk job application emails using a list of recipients from an Excel file. Each email can include attachments like CV, Cover Letter, and Reference Letters, and is sent asynchronously in the background using Celery.

 ---
## 📄 Project Description
This project automates the process of applying for jobs by sending out emails with attachments to multiple recipients, as listed in a provided Excel file. The backend is powered by **FastAPI** (for API endpoints) and **Celery** (for background task processing), with **Redis** acting as the message broker for Celery.

---
## 📁 Table Of Contents

    |
    |-main.py
    |-email_utils.py
    |-requirements.txt   <- Installs the required python pacakges
    |-README.md
    |-.gitignore
    |-.env               <- Holds Environment Variables, needs to be created
    |-.conda             <- Appears After creating an environment after cloning the project
## 🚀 Features
- ✅ Read recipient info from an Excel file

- ✅ Accept user credentials and email data via form (or API)

- ✅ Send personalized emails using `{name}` and `{company}` placeholders

- ✅ Attach multiple PDFs (CV, Cover Letter, Reference Letter)

- ✅ Execute email sending as background Celery task

- ✅ Secure with Authorization header

- ✅ Easily test with `curl` or frontend clients

 ---
## How to Install and Run the Project

### 1. Clone the Repository
    >> git clone https://github.com/your-username/job-bot-backend.git
    >> cd job-bot-backend
    
### 2. Create a Python Environment

    >> conda create -n jobbot python=3.10
	>> conda activate jobbot
	
### 3.Install the required Python dependencies

    >> pip install -r requirements.txt

### Create a `.env` File in the Root Directory

    AUTH_TOKEN=supersecrettoken123
 ---
 
## 🧪 How to Run the Project

### ✅ Start the FastAPI Server
	>> uvicorn app:app --reload

### ✅ Start the Redis Server
***If you’re using Docker (recommended):***

    >> docker run -d -p 6379:6379 --name redis redis

### ✅ Start the Celery Worker
💡*Use `--pool=solo` **only on Windows** during development.*

	# Windows (Dev)
	>> celery -A tasks worker --loglevel=info --pool=solo

	# Linux / macOS (or Dockerized deployment)
	>> celery -A tasks worker --loglevel=info

### 🧾 Example Curl Request

    >> curl -X POST http://localhost:8000/send-mails \
	    -H "Authorization: Bearer supersecrettoken123" \
	    -F "email=you@gmail.com" \
	    -F "password=your_app_password" \
	    -F "subject=My Job Application" \
	    -F "body=Dear {name}, I am applying to {company}." \
	    -F "cv=@attachments/CVs/my_cv.pdf" \
		-F "cover_letter=@attachments/CoverLetters/my_cover_letter.pdf" \
		-F "reference_letter=@attachments/ReferenceLetters/my_ref.pdf"
---
## ✅ How to Use the Project

 - Prepare your `applications.xlsx` file under `/data` with the following columns:
		A. Name
		B. Email
		C. Company
 - Start the server and Celery worker.
 - Make an API call (like the one above) using your frontend or curl.
 - The emails will be sent in the background and you’ll receive a `task_id`.
 - (Optional) You can add a `/task-status/{task_id}` endpoint to track the status of the background job.
 ----
## 📌 Notes
 - Do **not** commit your `.env` file.
    
- Do **not** use your real email password — use **app passwords** (Gmail or Outlook).
    
- This app is backend-only — you can connect it to a React, Flutter, or any other frontend client.
---
## ☁️ Deployment Options (Free)
You can deploy this backend using:
 - **Render** (recommended for full stack)
    
-   **Railway**
    
-   **Fly.io**
    
-   **Upstash Redis** (free Redis hosting for Celery)
---

## 👤 Author
Made by Sijan

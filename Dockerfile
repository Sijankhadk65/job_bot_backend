FROM python:3.11-slim

WORKDIR /app

COPY . /app 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]

FROM python:3.10

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY ./app /app

# Copy the wait-for-db script
COPY ./scripts/wait-for-db.sh /wait-for-db.sh

CMD ["/wait-for-db.sh", "db", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

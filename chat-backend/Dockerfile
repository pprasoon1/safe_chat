FROM python:3.11-slim


WORKDIR /app


# Install system deps
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*


# Copy requirements
COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


# Copy source
COPY . .


EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
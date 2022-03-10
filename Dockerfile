FROM python:3.9-alpine

COPY src/ .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.app:app"]
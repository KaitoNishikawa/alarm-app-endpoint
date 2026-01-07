FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000 

ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "api_stuff/get_raw_data_from_watch.py"]
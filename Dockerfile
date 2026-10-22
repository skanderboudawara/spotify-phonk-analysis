FROM python:3.14-alpine

WORKDIR /phonk-spotify

COPY requirements.txt .
RUN apk upgrade --no-cache && pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["python", "./app/main.py"]

FROM python:3.11.4

WORKDIR /phonk-spotify

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "./app/main.py"]


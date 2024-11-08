FROM python:3

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y ca-certificates

RUN pip install -r requirements.txt

COPY . .
FROM python:3.8

ARG TAG=local

WORKDIR /usr/app/

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY token.json token.json

ADD src/ src/
COPY app.py app.py

COPY .env .env

CMD [ "python","app.py" ]
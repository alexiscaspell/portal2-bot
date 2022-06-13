FROM python:3.8

ARG TAG=local

WORKDIR /usr/app/

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD src/ src/
COPY app.py app.py

CMD [ "python","app.py" ]
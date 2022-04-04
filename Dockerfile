FROM python:3.9.5-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -yyq netcat

RUN apt-get update \
    && apt-get install -y apt-utils gcc g++ tree

RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /usr/src/app/

RUN chmod +x entrypoint.sh

EXPOSE 8000
CMD ["./entrypoint.sh"]
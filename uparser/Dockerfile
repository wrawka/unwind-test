FROM python:3.11.2-slim

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN apt-get update && apt-get install make \
    && pip install -U pip && pip install -r requirements.txt

COPY . .

CMD [ "make", "start-app" ]

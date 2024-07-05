FROM python:alpine


RUN apk update && \
    apk add nano

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt


COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
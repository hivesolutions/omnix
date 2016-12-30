FROM hivesolutions/python:latest
MAINTAINER Hive Solutions

EXPOSE 8080

ENV LEVEL INFO
ENV SERVER netius
ENV SERVER_ENCODING gzip
ENV HOST 0.0.0.0
ENV PORT 8080
ENV DEBUG 0
ENV MONGOHQ_URL mongodb://localhost
ENV PYTHONPATH /src

ADD requirements.txt /
ADD src /src

RUN apk update && apk add libpng-dev libjpeg-turbo-dev libwebp-dev
RUN pip install -r /requirements.txt && pip install --upgrade netius

CMD ["/usr/bin/python", "/src/omnix/main.py"]

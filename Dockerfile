FROM python:3.6.8-alpine

LABEL maintainer='alexandre menezes <alexandre.fmenezes@gmail.com>'

WORKDIR /app

RUN apk add --no-cache curl \
                       postgresql-dev \
                       build-base && \
    rm -rf /var/cache/apk/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]


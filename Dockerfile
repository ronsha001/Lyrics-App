FROM python:alpine

RUN pip install Flask flask-cors redis requests

WORKDIR /app

ENV REDIS_DNS="localhost"
ENV REDIS_PORT=6379
ENV DEFAULT_EXECUTE_TIME=3600

COPY . .

ENTRYPOINT [ "python3", "main.py" ]
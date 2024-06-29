# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
CMD ["waitress-serve", "--host", "0.0.0.0", "app:app"]

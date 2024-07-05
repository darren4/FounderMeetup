# syntax=docker/dockerfile:1

FROM python:3.12.4-slim-bullseye
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
CMD ["waitress-serve", "--host", "0.0.0.0", "app:app"]

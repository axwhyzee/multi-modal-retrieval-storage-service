# Use the official Python image as base
FROM python:3.11-slim

ENV FLASK_APP="app.py" \
    FLASK_RUN_HOST="0.0.0.0" \
    FLASK_RUN_PORT="5000" 

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SECRET_KEY = INSERCURE_!kt6o_-969ptk30fq80vd1+8%#)cmx!nx3bo2con7=-z$a9ma_

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .
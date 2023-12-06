FROM python:3.9

ENV PYTHONDONTWRITTEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /homeland
COPY requiments.txt /temp/requiments.txt

RUN pip install -r /temp/requiments.txt

COPY homeland /homeland

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
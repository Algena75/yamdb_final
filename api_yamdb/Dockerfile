FROM python:3.7-slim

WORKDIR ./app

COPY requirements.txt .

RUN pip3 install -r ./requirements.txt

COPY . ./

COPY ./templates/redoc.yaml ./static/

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"] 

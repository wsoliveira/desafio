FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code/appdesafio/
COPY requirements.txt /code/appdesafio/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code/appdesafio/

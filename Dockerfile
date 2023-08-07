FROM python:3.11-slim
FROM mysql:8

WORKDIR /books-app_test
COPY . /books-app_test

RUN pip3 install --no-cache-dir -r requirements.txt

CMD exec gunicorn --workers 1 --threads 8 --timeout 0 books_app_test:app

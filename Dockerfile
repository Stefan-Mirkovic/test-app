FROM python:3.11-slim
FROM mysql:8

WORKDIR /books-app_test
COPY . /books-app_test

ENV INSTANCE_HOST="178.221.204.193"
ENV DB_USER="SM"
ENV DB_PASS="SM-user-sifra004"
ENV DB_PORT=3306

RUN pip3 install --no-cache-dir -r requirements.txt

#CMD ["python", "books_app_test.py"]

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 books_app_test:app
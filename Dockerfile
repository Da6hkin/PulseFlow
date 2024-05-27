FROM python:3.10

WORKDIR /app


COPY requirements.txt /app/
RUN pip install -r requirements.txt


COPY . /app/


COPY certs/django-selfsigned.crt /app/certs/
COPY certs/django-selfsigned.key /app/certs/

CMD ["python", "manage.py", "runserver_plus", "--cert-file", "/app/certs/django-selfsigned.crt", "--key-file", "/app/certs/django-selfsigned.key"]

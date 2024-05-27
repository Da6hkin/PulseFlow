FROM python:3.10

WORKDIR /app


COPY requirements.txt /app/
RUN pip install -r requirements.txt


COPY . /app/

COPY certs/django-selfsigned.crt /app/certs/
COPY certs/django-selfsigned.key /app/certs/

CMD ["gunicorn", "--certfile=/app/certs/django-selfsigned.crt", "--keyfile=/app/certs/django-selfsigned.key", "--bind", "0.0.0.0:8000", "myapp.wsgi:application"]
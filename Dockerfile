# Dockerfile
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

COPY entrypoint.sh /code/

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && exec python manage.py runserver 0.0.0.0:8000"]
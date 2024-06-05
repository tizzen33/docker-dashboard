FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b :80", "-w 3", "--access-logfile", "-", "--error-logfile", "-", "docker_dashboard.wsgi:application"]
FROM python:3.10

WORKDIR /app

COPY . /

RUN pip3 install -r /requirements.txt

ENTRYPOINT ["gunicorn", "--chdir", "/app", "app:app", "-w", "1", "--threads", "1", "-b", "0.0.0.0:8080"]

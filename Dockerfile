FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV FLASK_CONFIG=production

WORKDIR /app

COPY . .

RUN useradd -r ecowitt \
 && pip3 install --no-cache-dir --upgrade pip setuptools wheel \
 && pip3 install --no-cache-dir -r requirements.txt

USER ecowitt

ENTRYPOINT ["gunicorn", "--chdir", "/app", "main:app", "-w", "1", "--threads", "1", "-b", "0.0.0.0:7677"]

EXPOSE 7677

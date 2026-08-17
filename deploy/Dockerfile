FROM python:3.12-alpine

WORKDIR /app

COPY deploy/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY deploy/app.py /app/app.py
COPY site /app/site

# Never runs as root. docker-compose.yml overrides this with the host uid that
# owns the data volume; this is the fallback for anyone running the image bare.
RUN adduser -D -u 10001 ccdc
USER ccdc

ENV CCDC_SITE=/app/site \
    CCDC_DATA=/data \
    PYTHONUNBUFFERED=1

EXPOSE 8100

# Single worker keeps the in-memory rate limiter honest. This page will never
# need more; if it somehow does, move the limiter to the proxy.
CMD ["gunicorn", "--bind", "0.0.0.0:8100", "--workers", "1", "--threads", "4", \
     "--access-logfile", "-", "--error-logfile", "-", "app:app"]

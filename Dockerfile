FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# gettext -> tarjima, libjpeg/zlib -> rasm (Pillow), curl -> tekshirish
RUN apt-get update && apt-get install -y --no-install-recommends \
        gettext libjpeg62-turbo zlib1g curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh
RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8001

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
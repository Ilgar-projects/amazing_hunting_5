FROM python:3.13.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Минимальные системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
  && rm -rf /var/lib/apt/lists/*

# Зависимости (лучше кешируется)
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Код
COPY . .

# директории под статику/медиа (чтобы collectstatic и загрузки работали)
RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8000

# Миграции + статика + gunicorn
CMD ["sh","-c","python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn amazing_hunting_5.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2 --timeout 60"]

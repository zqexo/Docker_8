FROM python:3.11-slim

WORKDIR /code

# Установка обновлений и сертификатов
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Обновление pip
RUN pip install --upgrade pip

# Копирование requirements.txt и установка зависимостей
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Копирование остальных файлов
COPY . .

# Установка точки входа
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
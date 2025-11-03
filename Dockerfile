FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Установим postgresql-client для pg_isready
RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Создаём пользователя (до изменения владельца)
RUN adduser --disabled-password --gecos '' appuser

# Создаём папки для статики и медиа
RUN mkdir -p staticfiles
RUN mkdir -p uploads

# Меняем владельца папок на appuser
RUN chown -R appuser:appuser /app/staticfiles
RUN chown -R appuser:appuser /app/uploads

# Устанавливаем пользователя по умолчанию
USER appuser

# НЕ запускаем collectstatic или migrate при сборке
CMD ["gunicorn", "blog_project.wsgi:application", "--bind", "0.0.0.0:8000"]
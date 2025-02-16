# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем зависимости для сборки (curl для установки Poetry)
RUN apt-get update && \
    apt-get install -y curl build-essential && \
    apt-get clean

# Устанавливаем Poetry
ENV POETRY_VERSION=1.6.1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /test

# Копируем зависимости и устанавливаем их
COPY pyproject.toml poetry.lock /test/
RUN poetry install --only main --no-root

# Копируем код приложения
COPY avito /test/avito

# Открываем порт (8080, как указано в задании)
EXPOSE 8080

# Запускаем приложение
CMD ["poetry", "run", "uvicorn", "avito.main:main_app", "--host", "0.0.0.0", "--port", "8080"]

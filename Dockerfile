FROM python:3.12

# Устанавливаем зависимости для сборки (curl для установки Poetry)
RUN apt-get update && \
    apt-get install -y curl build-essential netcat-openbsd postgresql-client && \
    apt-get clean

# Устанавливаем Poetry
ENV POETRY_VERSION=1.6.1
RUN curl -sSL https://install.python-poetry.org | python3 - 
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY pyproject.toml poetry.lock /app/
RUN poetry install

# Копируем код приложения
COPY . .

# Копируем wait-for-it.sh в контейнер и даем права на выполнение
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Открываем порт (8080, как указано в задании)
EXPOSE 8080

# Запускаем приложение с ожиданием подключения к базе данных
CMD ["/wait-for-it", "pg:5432", "-t", "30", "--", "poetry", "run", "uvicorn", "avito.main:main_app", "--host", "0.0.0.0", "--port", "8080"]

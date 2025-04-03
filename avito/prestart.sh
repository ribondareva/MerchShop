#!/bin/bash

echo "Проверка миграций Alembic..."

if [ -f "/app/avito/alembic.ini" ]; then
    echo "Применение миграций..."
    poetry run alembic -c /app/avito/alembic.ini upgrade head
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "Миграции успешно применены!"
    else
        echo "Ошибка применения миграций!" >&2
        exit $exit_code
    fi
else
    echo "Файл alembic.ini не найден!" >&2
    exit 1
fi
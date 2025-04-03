#!/bin/bash

# Параметры подключения к БД
host="$1"
port="$2"
shift 2

# Функция для проверки доступности БД
wait_for_db() {
    echo "Ожидание доступности PostgreSQL на $host:$port..."
    until nc -z -v -w30 "$host" "$port"; do
        echo "Ждём $host:$port..."
        sleep 1
    done
    echo "PostgreSQL доступен!"
}

# Функция для выполнения миграций
run_migrations() {
    local prestart_script="/app/avito/prestart.sh"
    
    if [ -f "$prestart_script" ]; then
        echo "Найден скрипт prestart.sh, выполняем миграции..."
        chmod +x "$prestart_script"
        if "$prestart_script"; then
            echo "Миграции успешно выполнены!"
        else
            echo "Ошибка выполнения миграций!" >&2
            exit 1
        fi
    else
        echo "Скрипт prestart.sh не найден, пропускаем миграции."
    fi
}

# Основной процесс
wait_for_db
run_migrations

# Запуск основного приложения
echo "Запуск команды: $@"
exec "$@"
#!/bin/bash
# wait-for-it.sh
host="$1"
port="$2"
shift 2

# Wait for PostgreSQL to be available
until nc -z -v -w30 $host $port; do
  echo "Waiting for $host:$port to be available..."
  sleep 1
done

# Run the rest of the command after the database is available
exec "$@"

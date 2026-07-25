#!/bin/sh
set -e

echo "==> Migratsiya..."
python manage.py migrate --noinput

echo "==> Static yig'ish..."
python manage.py collectstatic --noinput --clear

echo "==> Ishga tushmoqda..."
exec "$@"
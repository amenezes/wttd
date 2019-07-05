#!/usr/bin/env sh

set -e

python manage.py collectstatic --no-input
python manage.py migrate

# exec gunicorn -w 2 -b 0.0.0.0:8000 eventex.wsgi --log-file -
exec python manage.py runserver 0.0.0.0:8000


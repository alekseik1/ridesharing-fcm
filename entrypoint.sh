#!/bin/sh
python manage.py migrate
# All CMD if processed afterwards
exec "$@"
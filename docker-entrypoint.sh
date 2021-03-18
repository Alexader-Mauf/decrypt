#!/bin/bash
sleep 15
python3 manage.py migrate
python3 manage.py collectstatic --noinput
exec "$@"
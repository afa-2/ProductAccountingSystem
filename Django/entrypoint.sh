#!/bin/bash

chmod ugo+rwx ./ProductAccountingSystem/manage.py

>&2 echo "Waiting for the db to be ready."

while ! ./ProductAccountingSystem/manage.py sqlflush > /dev/null 2>&1 ;do
    >&2 echo "Waiting for the db to be ready."
    sleep 1
  done

cd ProductAccountingSystem/

python3 ./manage.py makemigrations
python3 ./manage.py migrate
python3 ./manage.py collectstatic --noinput

uwsgi --socket :8001 --module ProductAccountingSystem.wsgi

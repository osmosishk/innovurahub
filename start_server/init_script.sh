cd ..
python3 manage.py runserver 0.0.0.0:8000 &
celery -A principal worker &
celery -A principal beat > /dev/null 2>&1 &


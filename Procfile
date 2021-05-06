web: python manage.py collectstatic --no-input; gunicorn django_project.wsgi --log-file - --log-level debug; release: python manage.py migrate



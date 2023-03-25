.PHONY: django-migrate django-start django-q django-init start-app 

django-migrate:
	python manage.py migrate

django-dev:
	python manage.py runserver

django-q:
	python manage.py qcluster

django-start:
	gunicorn config.wsgi -b 0.0.0.0:8000 --daemon

django-init: django-migrate
	python manage.py collectstatic --no-input

start-app: django-init django-start django-q


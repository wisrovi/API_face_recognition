MAKEFLAGS += --always-make

build:
	docker-compose build

up: build
	docker-compose up -d sidecar

upall: down build
	docker-compose up -d

app-coverage:
	docker-compose run --rm sidecar python -m pytest --cov=../app --cov-report html:coverage_html --cov-fail-under=100 --cov-config=pytest.ini

app-lint:
	docker-compose run --rm sidecar pylint ../app

app-flake8:
	docker-compose run --rm sidecar flake8 ../app

app-pyflake:
	docker-compose run --rm sidecar pyflakes ../app

app-test-dev:
	docker-compose run --rm sidecar ptw --config pytest.ini

down:
	docker-compose down

sidecar-bash:
	docker-compose run --rm sidecar bash

app-migrate:
	docker-compose run --rm sidecar python manage.py migrate

app-makemigrations:
	docker-compose run --rm sidecar python manage.py makemigrations

app-create-superuser:
	docker-compose run --rm sidecar python manage.py createsuperuserwithpassword --username admin --email admin@admin.com --password admin --preserve --force-color

app-runserver:
	docker-compose run --rm sidecar python manage.py runserver

app-requeriments:
	docker-compose run --rm sidecar pip freeze > src/requirements.txt
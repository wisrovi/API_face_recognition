MAKEFLAGS += --always-make

build:
	docker-compose build

up: build
	docker-compose up -d sidecar

upall: down build
	docker-compose up -d

app-coverage:
	docker-compose run --rm sidecar pytest --cov=app --cov-report=term-missing --cov-fail-under=100 --cov-config=pytest.ini

app-lint:
	docker-compose run --rm sidecar pylint ../app

app-test-dev:
	docker-compose run --rm sidecar ptw --config pytest.ini

down:
	docker-compose down

sidecar-bash:
	docker-compose run --rm sidecar bash

MAKEFLAGS += --always-make

build:
	docker-compose build

up: build
	docker-compose up -d sidecar

upall: down build
	docker-compose up -d

app-test-dev:
	docker-compose run --rm sidecar ptw --config pytest.ini

down:
	docker-compose down

sidecar-bash:
	docker-compose run --rm sidecar bash
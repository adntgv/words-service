all: .env start

.env:
	cp .env.example .env

start:
	docker compose up
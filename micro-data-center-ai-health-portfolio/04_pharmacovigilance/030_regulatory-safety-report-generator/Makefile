.PHONY: install test api docker

install:
	pip install -r requirements.txt

test:
	pytest -q

api:
	uvicorn src.api.main:app --reload

docker:
	docker compose up --build

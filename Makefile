.PHONY: install data train test api docker clean

install:
	pip install -r requirements.txt

data:
	python scripts/generate_sample_data.py

train:
	python -m src.models.train

test:
	pytest -q

api:
	uvicorn src.api.main:app --reload

docker:
	docker compose up --build

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '__pycache__']]"

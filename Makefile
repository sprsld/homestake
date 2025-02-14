deploy-local:
	. venv/bin/activate && pip install --no-cache-dir -r requirements.txt && fastapi dev homestake/main.py

deploy-ci:
	docker-compose up --build

test: clean
	. venv/bin/activate && pip install --no-cache-dir -r requirements.txt && rm -f ./homestake.db && pytest -v && deactivate

test-ci: clean
	docker-compose run --build --rm app pytest -v
	docker-compose down

clean:
	docker-compose down
	docker volume rm homestake_postgres_data || true
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '*.db' -delete

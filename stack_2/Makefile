setup:
	pipenv install --dev

tests:
	pipenv run pytest --cov=./

lint:
	cd src/ ; \
	pipenv run pylint jaffle/ jaffle_tests/

fmt:
	cd src/ ; \
	pipenv run isort jaffle/ jaffle_tests/ ; \
	pipenv run black jaffle/ jaffle_tests/

check_style:
	cd src/ ; \
	pipenv run black --check --diff jaffle/ jaffle_tests/ ; \
	pipenv run isort --check --diff jaffle/ jaffle_tests/ ; \
	pipenv run pylint jaffle/ jaffle_tests/

start_localstack: tests
	docker-compose up -d

apply_terraform: tests
	cd terraform/ ; \
	tflocal init ; \
	tflocal apply -auto-approve

start_dagster: tests
	cd src/ ; \
	pipenv run dagit
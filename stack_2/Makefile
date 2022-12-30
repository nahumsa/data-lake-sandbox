setup:
	pipenv install --dev

tests:
	pytest

start_localstack: tests
	docker-compose up -d

apply_terraform: tests
	cd terraform/ ; \
	tflocal init ; \
	tflocal apply -auto-approve

start_dagster: tests
	cd src/ ; \
	pipenv run dagit
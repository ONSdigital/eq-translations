build:
	pipenv install --dev

lint:
	pipenv run pylint eq_translations ./tests
	pipenv run black --check eq_translations tests

format:
	pipenv run black .

test:
	pipenv run pytest --cov-config=.coveragerc --cov --cov-report html tests

build:
	pipenv install --dev

lint:
	pipenv check ./eq_translations ./tests
	pipenv run pylint eq_translations ./tests
	pipenv run black --check .

test: lint
	pipenv run pytest --cov-config=.coveragerc --cov --cov-report html

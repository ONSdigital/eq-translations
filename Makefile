build:
	pipenv install --dev

lint:
	pipenv run pylint eq_translations ./tests
	pipenv run black --check eq_translations tests

test:
	pipenv run pytest --cov-config=.coveragerc --cov --cov-report html tests

install:
	pipenv install
	pipenv lock -r > requirements.txt

deploy: install
	./deploy.sh

run-debug:
	pipenv run functions-framework --target=check_translations --debug
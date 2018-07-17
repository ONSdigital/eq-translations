build:
	pipenv install --dev

lint:
	pipenv check ./app ./tests

test: lint
	pipenv run pytest ./tests
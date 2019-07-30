build:
	pipenv install --dev

lint:
	pipenv check ./eq_translations ./tests
	pylint eq_translations

test: lint
	pipenv run pytest ./tests

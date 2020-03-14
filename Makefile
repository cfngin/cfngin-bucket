clean:
	rm -rf .runway_cache/

lint: lint-flake8 lint-pylint lint-mypy lint-isort

lint-flake8:
	@echo "Running flake8..."
	@pipenv run flake8 .
	@echo ""

lint-isort:
	@echo "Running isort... If this fails, run 'make sort' to resolve."
	@pipenv run isort . --recursive --check-only
	@echo ""

lint-mypy:
	@echo "Running mypy..."
	@find . -name '*.py' -not -path '*.runway_cache/*' -not -path '*.venv/*' -exec pipenv run mypy {} +
	@echo ""

lint-pylint:
	@echo "Running pylint..."
	@find . -name '*.py' -not -path '*.runway_cache/*' -not -path '*.venv/*' | xargs pipenv run pylint --rcfile=setup.cfg
	@echo ""

sort:
	@pipenv run isort . --recursive --atomic

sync:
	PIPENV_VENV_IN_PROJECT=1 pipenv sync --dev --three

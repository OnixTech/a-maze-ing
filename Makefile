PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = default_config.txt

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$() -n pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports -

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict

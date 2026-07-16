PYTHON := uv run python
MAIN := a_maze_ing.py
CONFIG := default_config.txt

SRC = ./a_maze_ing.py ./config_parser.py

SYNC := .synced
INSTALL := .uv_installed


$(INSTALL): flake.lock
	python -m pip install uv
	@touch $(INSTALL)

$(SYNC): pyproject.toml
	uv sync || pip install uv && uv sync
	@touch $(SYNC)

install: $(SYNC)
	
run: install
	$(PYTHON) $(MAIN) $(CONFIG)

debug: $(SYNC)
	$(PYTHON) -n pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -f maze.txt

lint: $(SYNC)
	ruff check
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: $(SYNC)
	ruff check 
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict

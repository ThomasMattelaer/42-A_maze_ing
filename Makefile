NAME = a_maze_ing.py
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

run: install
	$(PYTHON) ${NAME}

clean:
	rm -rf .mypy_cache
	rm -rf __pycache__
	rm -rf venv

install: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

debug: install
	$(PYTHON) -m pdb ${NAME}

lint:
	flake8 --exclude=./venv .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 --exclude=./venv .
	mypy . --strict

.PHONY: run install clean lint lint-strict debug

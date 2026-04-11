PYTHON ?= python3

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .
	$(PYTHON) -m pip install flake8 mypy build

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; targets=['__pycache__','.mypy_cache','.pytest_cache','build','dist']; [shutil.rmtree(p, ignore_errors=True) for p in targets]; [shutil.rmtree(p, ignore_errors=True) for p in Path('.').glob('*.egg-info')]"

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

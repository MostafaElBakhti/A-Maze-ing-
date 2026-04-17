PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

install:
	pip install flake8 mypy build

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf *.pyc
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf mazegen.egg-info
	rm -rf test_env

lint:
	flake8 .
	mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
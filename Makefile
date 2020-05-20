EXECUTABLES = pip pipenv
K := $(foreach exec,$(EXECUTABLES),\
	$(if $(shell which $(exec)), ,$(error "Command '$(exec)' not found, condider installing.")))

PIPENV := $(shell command -v pipenv 2> /dev/null)

nothing:
	echo "Nothing done."

install:
ifdef PIPENV
	# pipenv found
	pipenv install -r requirements.txt
	pipenv install --dev -r requirements-dev.txt
else
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
endif

.PHONY: clean
clean:
	test -d dist && rm -rf dist/ || true
	test -d build && rm -rf build/ || true
	test -d python_homie4.egg-info && rm -rf python_homie4.egg-info || true
	find . -type d -name "__pycache__" -mindepth 1 -exec rm -rf {} \; -prune
	find . -type f -name "*.pyc" -exec rm {} \;

snapshot: 
ifdef PIPENV
	pipenv run python setup.py egg_info --tag-build=dev --tag-date sdist bdist_wheel bdist_egg && \
		$(MAKE) snapshot-version 
else
	python setup.py egg_info --tag-build=dev --tag-date sdist bdist_wheel bdist_egg && \
		$(MAKE) snapshot-version 
endif

dist: 
ifdef PIPENV
	pipenv run python setup.py sdist bdist_wheel bdist_egg
else
	python setup.py sdist bdist_wheel bdist_egg
endif

.PHONY: tests
tests: 
ifdef PIPENV
	pipenv run python -m pytest 
else
	python -m pytest 
endif

.PHONY: lint
lint: 
ifdef PIPENV
	pipenv run python -m pytest --pycodestyle
else
	python -m pytest --pycodestyle
endif

.PHONY: codestyle
codestyle: 
ifdef PIPENV
	pipenv run python -m flake8
else
	python -m flake8
endif

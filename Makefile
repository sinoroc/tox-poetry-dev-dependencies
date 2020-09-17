#


source_dir := ./src
tests_dir := ./test


.DEFAULT_GOAL := refresh


.PHONY: refresh
refresh: clean develop review package


.PHONY: develop
develop:
	python3 setup.py develop


.PHONY: package
package: sdist wheel


.PHONY: sdist
sdist:
	python3 setup.py sdist
	python3 -m twine check dist/*.tar.gz


.PHONY: wheel
wheel:
	python3 setup.py bdist_wheel
	python3 -m twine check dist/*.whl


.PHONY: format
format:
	python3 -m yapf --in-place --parallel --recursive setup.py src test


.PHONY: check
check:
	python3 setup.py check


.PHONY: lint
lint:
	python3 -m pytest --mypy --pycodestyle --pydocstyle --pylint --yapf \
		-m 'mypy or pycodestyle or pydocstyle or pylint or yapf'


.PHONY: mypy
mypy:
	python3 -m pytest --mypy -m mypy


.PHONY: pycodestyle
pycodestyle:
	python3 -m pytest --pycodestyle -m pycodestyle


.PHONY: pydocstyle
pydocstyle:
	python3 -m pytest --pydocstyle -m pydocstyle


.PHONY: pylint
pylint:
	python3 -m pytest --pylint -m pylint


.PHONY: yapf
yapf:
	python3 -m pytest --yapf -m yapf


.PHONY: test
test: pytest


.PHONY: pytest
pytest:
	python3 -m pytest


.PHONY: review
review: check
	python3 -m pytest --mypy --pycodestyle --pydocstyle --pylint --yapf


.PHONY: clean
clean:
	$(RM) --recursive ./.eggs/
	$(RM) --recursive ./.pytest_cache/
	$(RM) --recursive ./build/
	$(RM) --recursive ./dist/
	$(RM) --recursive ./__pycache__/
	find $(source_dir) -name '*.dist-info' -type d -exec $(RM) --recursive {} +
	find $(source_dir) -name '*.egg-info' -type d -exec $(RM) --recursive {} +
	find $(source_dir) -name '*.pyc' -type f -exec $(RM) {} +
	find $(tests_dir) -name '*.pyc' -type f -exec $(RM) {} +
	find $(source_dir) -name '__pycache__' -type d -exec $(RM) --recursive {} +
	find $(tests_dir) -name '__pycache__' -type d -exec $(RM) --recursive {} +


#
# Options
#

# Disable default rules and suffixes (improve speed and avoid unexpected behaviour)
MAKEFLAGS := --no-builtin-rules --warn-undefined-variables
.SUFFIXES:


# EOF

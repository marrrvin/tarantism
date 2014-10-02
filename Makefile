
ROOT_PATH=$(shell pwd)
PACKAGE_NAME=tarantism
PACKAGE_PATH=$(ROOT_PATH)/$(PACKAGE_NAME)
TESTS_PATH=$(ROOT_PATH)/tests

PIP_BIN=pip
PEP8_BIN=pep8

TEST_RUNNER=nosetests
TEST_RUNNER_ARGS=-v --nocapture
TEST_COVERAGE_REPORT_DIR=$(ROOT_PATH)/htmlcov/
TEST_COVERAGE_ARGS=--with-coverage --cover-package=$(PACKAGE_NAME) \
                   --cover-html --cover-html-dir=$(TEST_COVERAGE_REPORT_DIR)


all: help

help:
	@echo "help         - display this help."
	@echo "init         - install project requirements."
	@echo "inittest     - install tests requirements."
	@echo "test         - run tests"
	@echo "testcoverage - run tests with code coverage report."
	@echo "initdev      - install development tools."
	@echo "clean        - clean all artifacts."
	@echo "clean-build  - remove build artifacts."
	@echo "clean-pyc    - remove Python file artifacts."
	@echo "clean-tests  - remove tests running artifacts."
	@echo "check        - check package code style via pep8 utility."

init:
	$(PIP_BIN) install -r requirements.txt

inittest:
	$(PIP_BIN) install -r test-requirements.txt

test: init inittest
	MOCKERNAUT_SETTINGS=$(SETTINGS_PATH)/test_config.py \
	$(TEST_RUNNER) $(TEST_RUNNER_ARGS) $(TESTS_PATH)

testcoverage:
	$(TEST_RUNNER) $(TEST_RUNNER_ARGS) $(TEST_COVERAGE_ARGS) $(TESTS_PATH)

initdev:
	$(PIP_BIN) install -r dev-requirements.txt

clean: clean-build clean-pyc clean-tests

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-tests:
	rm -fr $(TEST_COVERAGE_REPORT_DIR)

check: initdev
	$(PEP8_BIN) $(PACKAGE_PATH) $(TESTS_PATH)

ROOT_DIR ?= $(CURDIR)
ACTIVATE := . $(ROOT_DIR)/venv/bin/activate &&
PROJECT := $(notdir $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))

install: venv
	$(ACTIVATE) pip install -e .

venv:
	python3 -m venv venv
	$(ACTIVATE) pip install -U pip
	$(ACTIVATE) pip install pip-compile-multi
	$(ACTIVATE) pip-compile-multi --autoresolve
	$(ACTIVATE) bash -c 'for req_file in requirements/*.txt; do pip install -r $$req_file; done'
	touch -c venv

start: install

test:
	$(ACTIVATE) pytest .

format:
	$(ACTIVATE) black $(PROJECT) tests app
	$(ACTIVATE) ruff check --fix $(PROJECT) tests app

app:
	 $(ACTIVATE) PYTHONPATH=. streamlit run app/app.py

docker-llama:
	docker-compose up -d

.PHONY: requirements start test format venv install app
# Makefile to ease trivial tasks for the project

VENV="$(shell find . -name ".*env")"
INVENV="$(shell which python | grep ${VENV})"
REQ="requirements.txt"


.PHONY: req-venv
# checks if virtual environment is activated and exits if it isn't 
req-venv:
ifeq (${INVENV}, "")
	$(error Virtual environment not activated)
endif


.PHONY: run
run: req-venv
	# run the Flask server
	@python close_crawl/server.py


.PHONY: installenv
installenv:
	# install the virtual environment
	@test -d $(VENV) && virtualenv $(VENV) || virtualenv .venv


.PHONY: init
init: req-venv
	# upgrade PIP on virtual environment
	@pip install -U pip && pip install -r ${REQ}


.PHONY: update
update: req-venv
	# update PIP requirements
	@pip freeze | grep -Eiv "pkg-resources|pyinstaller|nose" > ${REQ}


.PHONY: clean
clean:
	# remove Python cache and temporary files
	@find . \( -name "*.pyc" -type f -o -name "__pycache__" -type d \) -delete
	@find . \( -name "test_output.csv" -o -name "port.txt" \
		-o -name "checkpoint.json" \) -type f -delete


.PHONY: test
test: req-venv
	# run backend unit tests
	@nosetests -v -w tests && rm -rf "tests/test_output.csv" "tests/responses/"

# Makefile to ease trivial tasks for the project

VENV="$(shell find . -name ".*env")"
IN_VENV="$(shell [ "/usr/local/bin/python" = $(shell which python) ] && \
	echo 0 || echo 1)"
REQ=requirements.txt


.PHONY: run
run:
	# run the Flask server
	@python close_crawl/server.py


.PHONY: clean
clean:
	# remove Python cache and temporary files
	@find . \( \
		-name "*.pyc" -o -name "test_output.csv" -o -name "port.txt" \
		-o -name "checkpoint.json" -o -name "*.aux" -o -name "*.log" \
		\) -type f -delete
	@find -name "__pycache__" -type d -delete


.PHONY: test
test:
	# run backend unit tests
	@nosetests -v -w tests && rm -rf "tests/test_output.csv" "tests/responses/"


.PHONY: install
install:
	# install the virtual environment
	@test -d $(VENV) && virtualenv $(VENV) || virtualenv .venv


.PHONY: upgrade
upgrade:
	# upgrade PIP on virtual environment
	@test 1 -eq $(IN_VENV) && pip install -U pip && pip install -r $(REQ) \
	|| echo 'Activate virtual environment first'


.PHONY: update
update:
	# update PIP requirements
	@test 1 -eq $(IN_VENV) && pip freeze | grep -Ev "PyInstaller|nose" > $(REQ) \
	|| echo 'Activate virtual environment first'


.PHONY: cache_convert convert1 convert2
cache_convert: convert1 convert2
convert1 convert2:
	# convert LaTex file to PDF
	@sudo pdflatex test.tex


.PHONY: changeown
changeown:
	# change file permissions
	@sudo chown -R $(USER) .

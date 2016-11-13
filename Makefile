# Makefile to ease trivial tasks for the project

VENV="$(shell find . -name ".*env")"
IN_VENV="$(shell python venv.py)"
REQ=requirements.txt

.PHONY: install
install:
	# install the virtual environment
	@test -d $(VENV) && virtualenv $(VENV) || virtualenv .venv


.PHONY: clean
clean:
	# clean out Python cache and temporary files
	@find . \( -name "*.pyc" -o -name "test_out.csv" \) -type f -delete


.PHONY: upgrade
upgrade:
	# upgrade PIP on virtual environment
	@test 1 -eq $(IN_VENV) && pip install -U pip && pip install -r $(REQ) \
	|| echo 'Activate virtual environment first'


.PHONY: update
update:
	# update PIP requirements
	@test 1 -eq $(IN_VENV) && pip freeze > $(REQ) \
	|| echo 'Activate virtual environment first'


# no tests yet
# .PHONY: test
# test:
# 	# run backend unit tests
# 	@nosetests -v tests

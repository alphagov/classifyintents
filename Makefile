## Sample makefile from http://docs.python-guide.org/en/latest/writing/structure/

init:
	pip install -r requirements.txt

local:
	pip install -e ./
update:
	pip install git+git://github.com/ivyleavedtoadflax/classify.git@dev --upgrade

test:
	nosetests

.PHONY: init test

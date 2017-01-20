pep8:
	flake8 takayi tests

test: pep8
	rm -rf .cache
	mkdir -p .build
	py.test tests -rfExswX --duration=10 --junitxml=.build/unittest.xml --cov takayi --cov-report xml -n 4
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

tag:
	@t=`python setup.py  --version`;\
	echo v$$t; git tag v$$t

clear_pyc:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

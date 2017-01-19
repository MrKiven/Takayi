pep8:
	flake8 type_doctor tests

test: pep8
	rm -rf .cache
	mkdir -p .build
	py.test tests -rfExswX --duration=10 --junitxml=.build/unittest.xml --cov type_doctor --cov-report xml -n 4
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

tag:
	@t=`python setup.py  --version`;\
	echo v$$t; git tag v$$t

clear_pyc:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

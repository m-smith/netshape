install:
	python setup.py install
test:
	cd ./src; python -m netshape.test.main

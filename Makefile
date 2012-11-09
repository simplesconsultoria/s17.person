# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

pep8_ignores = E501
options = -N -q -t 3

prerequisites:
	sudo apt-get install -qq pep8 pyflakes
	mkdir -p buildout-cache/downloads

install: prerequisites
	python bootstrap.py -c travis.cfg
	bin/buildout -c travis.cfg $(options)

tests:
	bin/createzopecoverage
	pep8 --ignore=$(pep8_ignores) src/s17
	# XXX: use patched version of pyflakes
	bin/pyflakes src/s17
	# FIXME: make: execvp: ./coverage: Permission denied
	#./coverage
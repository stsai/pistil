.PHONY: dist
dist: clean
	python setup.py -q sdist

.PHONY: rpm
rpm: dist
	rpmbuild --define="_rpmdir dist" --define="_sourcedir `pwd`/dist" \
		-ba --clean --quiet rpm.spec

.PHONY: clean
clean:
	rm -rf dist
	rm -f MANIFEST
	find . -name '*.pyc' -exec rm -f {} +

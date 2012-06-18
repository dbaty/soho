##
## Makefile (for developers)
##

package_name = soho
## WARNING: tmp_dir is deleted in the 'clean' rule. Be sure not to use
## "/tmp", "." or any directory that may contain anything else.
tmp_dir = /tmp/$(package_name)-distcheck
tmp_src_dir = $(tmp_dir)/src
tmp_cov_dir = $(tmp_dir)/coverage-output
tmp_env_dir = $(tmp_dir)/testing-env

.PHONY: coverage
coverage:
	coverage run setup.py test -q
	coverage html -d "$(tmp_cov_dir)"
	open "$(tmp_cov_dir)/index.html"
	@echo "Coverage information is available at '$(tmp_cov_dir)'."

cov: coverage

.PHONY: dist
dist:
	python setup.py sdist

# FIXME: 'distcheck' is not useful anymore now that we use 'tox'
.PHONY: distcheck
distcheck: clean dist
	virtualenv --no-site-packages $(tmp_env_dir)
	$(tmp_env_dir)/bin/easy_install Nose
	$(tmp_env_dir)/bin/easy_install Coverage
	mkdir -p $(tmp_src_dir)
	@name=`python setup.py --name` && \
		ver=`python setup.py --version` && \
		tar xfz ./dist/$$name-$$ver.tar.gz -C $(tmp_src_dir) && \
		cd $(tmp_src_dir)/$$name-$$ver && \
		$(tmp_env_dir)/bin/python setup.py install && \
		$(tmp_env_dir)/bin/python setup.py test

.PHONY:	qa
qa:
	pep8 -r setup.py || true
	pep8 -r $(package_name) || true
	pyflakes setup.py
	pyflakes $(package_name)

.PHONY: test
test:
	PYTHONWARNINGS=all python setup.py test

.PHONY: upload
upload:
	python setup.py sdist upload

.PHONY: clean
clean:
	rm -rf .coverage
	rm -rf ./dist/
	rm -rf $(tmp_dir)
	rm -rf .tox
	rm -f coverage.xml
	rm -f nosetests.xml
	find . -name "*.pyc" | xargs rm -f
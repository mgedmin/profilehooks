PYTHON = python
FILE_WITH_METADATA = profilehooks.py
FILE_WITH_VERSION = profilehooks.py
FILE_WITH_CHANGELOG = CHANGES.rst

.PHONY: default
default:
	@echo "Nothing to build here"

.PHONY: test check
test check:
	$(PYTHON) test_profilehooks.py

.PHONY: coverage
coverage:
	coverage run --source=profilehooks test_profilehooks.py
	coverage report

.PHONY: test-all-pythons
test-all-pythons:
	# poor man's tox -- why not use the real thing instead?
	set -e; \
	for ver in 2.6 2.7 3.0 3.1 3.2 3.3 3.4 3.5; do \
		if which python$$ver > /dev/null; then \
			$(MAKE) test PYTHON=python$$ver; \
		else \
			echo "=================================="; \
			echo "Skipping python$$ver, not available."; \
			echo "=================================="; \
		fi; \
	done

.PHONY: preview-pypi-description
preview-pypi-description:
	# pip install restview, if missing
	restview -e "$(PYTHON) setup.py --long-description"

.PHONY: dist
dist:
	$(PYTHON) setup.py -q sdist

.PHONY: distcheck
distcheck:
	# Bit of a chicken-and-egg here, but if the tree is unclean, make
	# distcheck will fail.
	@test -z "`git status -s 2>&1`" || { echo; echo "Your working tree is not clean" 1>&2; git status; exit 1; }
	make dist
	pkg_and_version=`$(PYTHON) setup.py --name`-`$(PYTHON) setup.py --version` && \
	rm -rf tmp && \
	mkdir tmp && \
	git archive --format=tar --prefix=tmp/tree/ HEAD | tar -xf - && \
	cd tmp && \
	tar xvzf ../dist/$$pkg_and_version.tar.gz && \
	diff -ur $$pkg_and_version tree -x PKG-INFO -x setup.cfg -x '*.egg-info' && \
	cd $$pkg_and_version && \
	make dist check && \
	cd .. && \
	mkdir one two && \
	cd one && \
	tar xvzf ../../dist/$$pkg_and_version.tar.gz && \
	cd ../two/ && \
	tar xvzf ../$$pkg_and_version/dist/$$pkg_and_version.tar.gz && \
	cd .. && \
	diff -ur one two -x SOURCES.txt && \
	cd .. && \
	rm -rf tmp && \
	echo "sdist seems to be ok"

.PHONY: releasechecklist
releasechecklist:
	@date_line='__date__ = "'`date +%Y-%m-%d`'"' && \
	    grep -q "^$$date_line$$" $(FILE_WITH_METADATA) || { \
	        echo "$(FILE_WITH_METADATA) doesn't specify $$date_line"; exit 1; }
	@$(PYTHON) setup.py --version | grep -qv dev || { \
	    echo "Please remove the 'dev' suffix from the version number in $(FILE_WITH_VERSION)"; exit 1; }
	@$(PYTHON) setup.py --long-description | rst2html --exit-status=2 > /dev/null
	@ver_and_date="`$(PYTHON) setup.py --version` (`date +%Y-%m-%d`)" && \
	    grep -q "^$$ver_and_date$$" $(FILE_WITH_CHANGELOG) || { \
	        echo "$(FILE_WITH_CHANGELOG) has no entry for $$ver_and_date"; exit 1; }
	make distcheck

.PHONY: release
release: releasechecklist
	# I'm chicken so I won't actually do these things yet
	@echo "Please run"
	@echo
	@echo "  rm -rf dist && $(PYTHON) setup.py -q sdist bdist_wheel && twine upload dist/* && git tag `$(PYTHON) setup.py --version`"
	@echo
	@echo "Please increment the version number in $(FILE_WITH_VERSION)"
	@echo "and add a new empty entry at the top of the changelog in $(FILE_WITH_CHANGELOG), then"
	@echo
	@echo '  git commit -a -m "Post-release version bump" && git push && git push --tags'
	@echo

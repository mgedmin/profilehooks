PYTHON = python

SUPPORTED_PYTHON_VERSIONS = 2.7 3.3 3.4 3.5 3.6

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
	coverage report -m --fail-under=100

.PHONY: test-all-pythons
test-all-pythons:
	# poor man's tox -- why not use the real thing instead?
	set -e; \
	for ver in $(SUPPORTED_PYTHON_VERSIONS); do \
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
	restview --long-description


.PHONY: releasechecklist
releasechecklist: check-date  # also release.mk will add other checks

include release.mk

.PHONY: check-date
check-date:
	@date_line='__date__ = "'`date +%Y-%m-%d`'"' && \
	    grep -q "^$$date_line$$" $(FILE_WITH_METADATA) || { \
	        echo "$(FILE_WITH_METADATA) doesn't specify $$date_line"; exit 1; }

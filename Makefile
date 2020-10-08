PYTHON = python3

FILE_WITH_METADATA = profilehooks.py
FILE_WITH_VERSION = profilehooks.py
FILE_WITH_CHANGELOG = CHANGES.rst

.PHONY: default
default:
	@echo "Nothing to build here"

.PHONY: flake8
flake8:
	tox -e flake8

.PHONY: test check
test check:
	tox -p auto

.PHONY: coverage
coverage:
	tox -e coverage,coverage3

.PHONY: preview-pypi-description
preview-pypi-description:
	# pip install restview, if missing
	restview --long-description


.PHONY: releasechecklist
releasechecklist: check-date  # also release.mk will add other checks

DISTCHECK_DIFF_OPTS = $(DISTCHECK_DIFF_DEFAULT_OPTS) -x .github
include release.mk

.PHONY: check-date
check-date:
	@date_line='__date__ = "'`date +%Y-%m-%d`'"' && \
	    grep -q "^$$date_line$$" $(FILE_WITH_METADATA) || { \
	        echo "$(FILE_WITH_METADATA) doesn't specify $$date_line"; \
	        echo "Please run make update-date"; exit 1; }

.PHONY: update-date
update-date:
	sed -i -e 's/^__date__ = ".*"/__date__ = "'`date +%Y-%m-%d`'"/' $(FILE_WITH_METADATA)

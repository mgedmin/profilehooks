.PHONY: all
all:
	@echo "Nothing to build here"

.PHONY: test
test:                           ##: run tests
	tox -p auto

.PHONY: coverage
coverage:                       ##: measure test coverage
	tox -e coverage

.PHONY: flake8
flake8:                         ##: check for style problems
	tox -e flake8


.PHONY: releasechecklist
releasechecklist: check-date  # also release.mk will add other checks

FILE_WITH_METADATA = profilehooks.py
FILE_WITH_VERSION = profilehooks.py
include release.mk

.PHONY: check-date
check-date:
	@date_line='__date__ = "'`date +%Y-%m-%d`'"' && \
	    grep -q "^$$date_line$$" $(FILE_WITH_METADATA) || { \
	        echo "$(FILE_WITH_METADATA) doesn't specify $$date_line"; \
	        echo "Please run make update-date"; exit 1; }

.PHONY: update-date
update-date:                    ##: set release date in source code to today
	sed -i -e 's/^__date__ = ".*"/__date__ = "'`date +%Y-%m-%d`'"/' $(FILE_WITH_METADATA)

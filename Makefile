# make html            build into build/html
# make live            rebuild on change (needs sphinx-autobuild)
# NN_DOCS_GITHUB_OWNER=<org> make html   build with other repository links (see source/conf.py)
SPHINX ?= .venv/bin/sphinx-build
html:
	$(SPHINX) -W --keep-going -b html source build/html
clean:
	rm -rf build
live:
	.venv/bin/sphinx-autobuild source build/html
.PHONY: html clean live

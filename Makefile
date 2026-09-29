# make html            build into build/html
# make live            rebuild on change (needs sphinx-autobuild)
# NN_DOCS_GITHUB_OWNER=<org> make html   build with other repository links (see source/conf.py)
SPHINX ?= .venv/bin/sphinx-build
html:
	$(SPHINX) -a -W --keep-going -b html source build/html   # -a: every page rewritten, so the sidebar never goes stale
clean:
	rm -rf build
live:
	.venv/bin/sphinx-autobuild source build/html
.PHONY: html clean live

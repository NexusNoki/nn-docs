"""@@name@@ substitution from conf.NN_VARS, applied to the raw page text
before it is parsed — so it works in prose, links AND code blocks (MyST's own
substitutions do not reach inside code fences).

An unknown name is a build warning, so a typo cannot ship silently.
Write \\@@name@@ to show the token itself (it renders as @@name@@).
"""
from __future__ import annotations

import re

from sphinx.util import logging

log = logging.getLogger(__name__)
_TOKEN = re.compile(r"(\\?)@@([a-z0-9_]+)@@")


def _replace(app, docname, source):
    values = app.config.nn_vars

    def sub(m):
        if m.group(1):
            return m.group(0)[1:]
        key = m.group(2)
        if key not in values:
            log.warning("unknown nn variable @@%s@@", key, location=docname)
            return m.group(0)
        return str(values[key])

    source[0] = _TOKEN.sub(sub, source[0])


def setup(app):
    app.add_config_value("nn_vars", {}, "env")      # conf.py sets nn_vars = NN_VARS
    app.connect("source-read", _replace)
    return {"version": "1", "parallel_read_safe": True}

"""Sphinx configuration for the nn documentation.

Everything that will change when the repositories go public lives in
NN_VARS below: the GitHub owner, repository names and the release links the
tutorial points at.  Each value can also be overridden at build time with an
environment variable, so a public build needs no source edits:

    NN_DOCS_GITHUB_OWNER=nn-project make html

Inside any page (prose, code blocks, links) write  @@name@@  and it is
replaced with the value before the page is parsed — see _ext/nn_vars.py.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

project = "nn"
author = "nn project"
copyright = "2026, nn project"
release = "0.1"

# ── values that change when the repositories become public ──────────────────
# key -> (default, environment variable that overrides it)
_VAR_DEFAULTS = {
    # Where the source and the release images live.  Private today, under a
    # personal account; a public organisation later.
    "github_owner":        ("chalos",                    "NN_DOCS_GITHUB_OWNER"),
    "github_host":         ("https://github.com",        "NN_DOCS_GITHUB_HOST"),
    # repositories
    "repo_hub":            ("nn-hub",                    "NN_DOCS_REPO_HUB"),
    "repo_modules":        ("nn-modules",                "NN_DOCS_REPO_MODULES"),
    "repo_camera_byai":    ("nn-app-camera-beagleyai-imx708", "NN_DOCS_REPO_CAMERA_BYAI"),
    # release (catalog) repositories the hub's Factory reads images from.
    # One repository per image, named after the image.
    "rel_sensor":          ("nn-app-mdns-ot-esp32c6",    "NN_DOCS_REL_SENSOR"),
    "rel_ncp":             ("nn-app-ncp-esp32c6",        "NN_DOCS_REL_NCP"),
    "rel_cam_p4_wifi6":    ("nn-app-camera-esp32p4-wifi6-sdio-ov5647", "NN_DOCS_REL_CAM_P4_WIFI6"),
    "rel_cam_p4_module":   ("nn-app-camera-esp32p4module-sdio-ov5647", "NN_DOCS_REL_CAM_P4_MODULE"),
    "rel_byai_sdcard":     ("byai_sdcard",               "NN_DOCS_REL_BYAI_SDCARD"),
    # an example hub address used throughout the tutorial
    "hub_ip":              ("192.168.1.50",              "NN_DOCS_HUB_IP"),
    "media_ip":            ("192.168.1.51",              "NN_DOCS_MEDIA_IP"),
}
NN_VARS = {k: os.environ.get(env, default) for k, (default, env) in _VAR_DEFAULTS.items()}
# derived values: always built from the ones above, never written twice
NN_VARS["github_base"] = f"{NN_VARS['github_host']}/{NN_VARS['github_owner']}"
for _k in list(NN_VARS):
    if _k.startswith(("repo_", "rel_")):
        NN_VARS[_k + "_url"] = f"{NN_VARS['github_base']}/{NN_VARS[_k]}"
        if _k.startswith("rel_"):
            NN_VARS[_k + "_releases"] = f"{NN_VARS['github_base']}/{NN_VARS[_k]}/releases"
# whether the repositories are public yet (changes a few sentences)
NN_VARS["repos_public"] = os.environ.get("NN_DOCS_REPOS_PUBLIC", "no")
nn_vars = NN_VARS           # read by _ext/nn_vars.py

# ── Sphinx ───────────────────────────────────────────────────────────────────
extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinxcontrib.mermaid",
    "sphinx.ext.todo",
    "nn_vars",          # @@name@@ substitution, from NN_VARS
    "nn_photos",        # {photo-needed} placeholders + the photo checklist page
]
myst_enable_extensions = ["colon_fence", "deflist", "attrs_inline", "attrs_block", "substitution", "tasklist"]
myst_heading_anchors = 3
source_suffix = {".md": "markdown"}
exclude_patterns = ["_build", ".venv"]
todo_include_todos = True           # unverified facts are marked {todo} and listed on one page

html_theme = "furo"
html_title = "nn documentation"
html_static_path = ["_static"]
html_css_files = ["nn.css"]
html_theme_options = {
    "source_repository": NN_VARS["repo_hub_url"] if NN_VARS["repos_public"] == "yes" else "",
    "navigation_with_keys": True,
}
copybutton_prompt_text = r"^\$ "
copybutton_prompt_is_regexp = True

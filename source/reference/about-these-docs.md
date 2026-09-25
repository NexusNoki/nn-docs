# About these docs

The manual is built with [Sphinx](https://www.sphinx-doc.org) from Markdown (MyST).

## Build

```console
$ python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
$ make html            # → build/html/index.html
```

## Links that will change

The source repositories and the release (catalog) repositories are private today, under the
account **@@github_owner@@**. They will become public under another account. Every GitHub link in
this manual is built from variables in `source/conf.py`, so the move needs no page edits:

| Variable | Current value | Override at build time |
|---|---|---|
| `github_owner` | `@@github_owner@@` | `NN_DOCS_GITHUB_OWNER` |
| `github_host` | `@@github_host@@` | `NN_DOCS_GITHUB_HOST` |
| `repo_hub` | `@@repo_hub@@` | `NN_DOCS_REPO_HUB` |
| `repo_modules` | `@@repo_modules@@` | `NN_DOCS_REPO_MODULES` |
| `repo_camera_byai` | `@@repo_camera_byai@@` | `NN_DOCS_REPO_CAMERA_BYAI` |
| `rel_sensor` | `@@rel_sensor@@` | `NN_DOCS_REL_SENSOR` |
| `rel_ncp` | `@@rel_ncp@@` | `NN_DOCS_REL_NCP` |
| `rel_cam_p4_wifi6` | `@@rel_cam_p4_wifi6@@` | `NN_DOCS_REL_CAM_P4_WIFI6` |
| `rel_cam_p4_module` | `@@rel_cam_p4_module@@` | `NN_DOCS_REL_CAM_P4_MODULE` |
| `rel_byai_sdcard` | `@@rel_byai_sdcard@@` | `NN_DOCS_REL_BYAI_SDCARD` |
| `hub_ip` | `@@hub_ip@@` | `NN_DOCS_HUB_IP` |
| `media_ip` | `@@media_ip@@` | `NN_DOCS_MEDIA_IP` |
| `repos_public` | `@@repos_public@@` | `NN_DOCS_REPOS_PUBLIC` (`yes` shows the source link in the page header) |

Each `repo_*` and `rel_*` variable also gives `<name>_url` (the repository page), and each `rel_*` gives `<name>_releases` (its releases page).

```console
$ NN_DOCS_GITHUB_OWNER=<new-org> NN_DOCS_REPOS_PUBLIC=yes make html
```

In a page, write `\@@name@@` for any variable — it is replaced everywhere, code blocks included,
and an unknown name fails the build.

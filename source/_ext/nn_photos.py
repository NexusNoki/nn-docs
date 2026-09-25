"""Photo placeholders.

    :::{photo-needed} Short title of the shot
    :id: hub-usb-gateway
    What the photo must show, from which angle, which labels must be readable.
    :::

renders a clearly marked box ("Photo needed") in the page, and

    :::{photo-list}
    :::

renders the checklist of every placeholder in the whole manual, each linking
back to its page — the list the photographer works from.  When the photo
exists, replace the directive with a normal image:

    ```{figure} /_static/photos/hub-usb-gateway.jpg
    :alt: …
    ```
"""
from __future__ import annotations

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective


class photo_needed(nodes.Admonition, nodes.Element):
    pass


class photo_list(nodes.General, nodes.Element):
    pass


class PhotoNeeded(SphinxDirective):
    required_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {"id": directives.unchanged}

    def run(self):
        title = self.arguments[0]
        pid = self.options.get("id") or nodes.make_id(title)
        target = nodes.target("", "", ids=[f"photo-{pid}"])
        node = photo_needed("\n".join(self.content))
        node["classes"] += ["admonition", "photo-needed"]
        node += nodes.title("", f"Photo needed: {title}")
        self.state.nested_parse(self.content, self.content_offset, node)
        env = self.env
        if not hasattr(env, "nn_photos"):
            env.nn_photos = []
        env.nn_photos.append({"docname": env.docname, "id": f"photo-{pid}", "title": title,
                              "text": " ".join(self.content).strip()})
        return [target, node]


class PhotoList(SphinxDirective):
    def run(self):
        return [photo_list("")]


def _purge(app, env, docname):
    if hasattr(env, "nn_photos"):
        env.nn_photos = [p for p in env.nn_photos if p["docname"] != docname]


def _merge(app, env, docnames, other):
    if not hasattr(env, "nn_photos"):
        env.nn_photos = []
    env.nn_photos.extend(getattr(other, "nn_photos", []))


def _resolve(app, doctree, fromdocname):
    photos = sorted(getattr(app.builder.env, "nn_photos", []), key=lambda p: (p["docname"], p["title"]))
    for node in doctree.findall(photo_list):
        if not photos:
            node.replace_self(nodes.paragraph(text="No photos outstanding."))
            continue
        lst = nodes.enumerated_list()
        for p in photos:
            item = nodes.list_item()
            para = nodes.paragraph()
            ref = nodes.reference("", "", internal=True,
                                  refuri=app.builder.get_relative_uri(fromdocname, p["docname"]) + "#" + p["id"])
            ref += nodes.strong(text=p["title"])
            para += ref
            title = app.builder.env.titles.get(p["docname"])
            para += nodes.Text(f"  ({title.astext() if title else p['docname']})")
            item += para
            if p["text"]:
                item += nodes.paragraph(text=_plain(p["text"]))
            lst += item
        node.replace_self(lst)


def _env_updated(app, env):
    """The photo list depends on every page: rewrite the pages holding it on each build."""
    return [d for d in env.found_docs
            if "photo-list" in open(env.doc2path(d), encoding="utf-8").read()]


def _plain(text):
    return text.replace("**", "").replace("*", "").replace("`", "")


def _visit(self, node):
    self.visit_admonition(node)


def _depart(self, node):
    self.depart_admonition(node)


def setup(app):
    app.add_node(photo_needed, html=(_visit, _depart), latex=(_visit, _depart), text=(_visit, _depart))
    app.add_node(photo_list)
    app.add_directive("photo-needed", PhotoNeeded)
    app.add_directive("photo-list", PhotoList)
    app.connect("env-purge-doc", _purge)
    app.connect("env-merge-info", _merge)
    app.connect("doctree-resolved", _resolve)
    app.connect("env-updated", _env_updated)
    return {"version": "1", "parallel_read_safe": True, "env_version": 1}

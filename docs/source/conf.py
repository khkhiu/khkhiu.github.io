# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'khkhiu.github.io'
copyright = '2026, Khiu Kim Hong'
author = 'Khiu Kim Hong'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser']

templates_path = ['_templates']
exclude_patterns = ["_posts_toc.rst", ]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

myst_heading_anchors = 3

# --- Auto-generate the posts toctree, newest first, from each post's "date:" front matter ---
import re
from pathlib import Path

def _write_posts_toc(app):
    src = Path(app.srcdir)
    posts = []
    for p in (src / "posts").glob("*.md"):
        text = p.read_text(encoding="utf-8")
        fm = re.match(r"---\s*\n(.*?)\n---", text, re.S)
        d = re.search(r"^date:\s*['\"]?(\d{4}-\d{2}-\d{2})", fm.group(1), re.M) if fm else None
        posts.append((d.group(1) if d else "0000-00-00", p.stem))
    posts.sort(reverse=True)
    lines = [".. toctree::", "   :maxdepth: 1", "   :caption: Posts", ""]
    lines += [f"   posts/{stem}" for _, stem in posts]
    new = "\n".join(lines) + "\n"
    out = src / "_posts_toc.rst"
    if not out.exists() or out.read_text(encoding="utf-8") != new:
        out.write_text(new, encoding="utf-8")

def setup(app):
    app.connect("builder-inited", _write_posts_toc)
exclude_patterns = ["_posts_toc.rst"]

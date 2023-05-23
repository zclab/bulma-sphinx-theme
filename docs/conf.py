import sys
from os.path import abspath, join, dirname
import bulma_sphinx_theme

sys.path.insert(0, abspath(join(dirname(__file__), "../src")))

project = "A sphinx theme based on bulma"
copyright = "2023"
author = "zclab"
master_doc = "index"
version = bulma_sphinx_theme.__version__
language = "en"  #'zh_CN'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinx_inline_tabs",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinx_subfigure",
]


myst_enable_extensions = ["colon_fence", "deflist"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.9", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    "markdown_it": ("https://markdown-it-py.readthedocs.io/en/latest", None),
}

templates_path = ["_templates"]
html_static_path = ["_static"]
html_theme = "bulma_sphinx_theme"
html_title = "A sphinx theme on bulma"
html_favicon = "_static/favicon.png"
html_last_updated_fmt = ""
html_logo = "_static/logo-.png"
html_show_sourcelink = True

todo_include_todos = True

# https://github.com/hung1001/font-awesome-pro-v6
html_css_files = [
    "https://cdn.jsdelivr.net/gh/duyplus/fontawesome-pro/css/all.min.css",
]

html_theme_options = {
    "header_links_before_dropdown": 2,
}

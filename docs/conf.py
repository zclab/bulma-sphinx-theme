import sys
import datetime
from os.path import abspath, join, dirname
import bulma_sphinx_theme

sys.path.insert(0, abspath(join(dirname(__file__), "../src")))

project = "A sphinx theme based on bulma"
author = "zclab"
year = str(datetime.date.today().year)
copyright = year + " " + author
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
    "bulma_sphinx_theme.demo.sphinxext",
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
html_logo = "_static/logo.svg"
html_show_sourcelink = True

todo_include_todos = True

# https://github.com/hung1001/font-awesome-pro-v6
html_css_files = [
    "https://cdn.jsdelivr.net/gh/duyplus/fontawesome-pro/css/all.min.css",
]

html_theme_options = {
    "header_links_before_dropdown": 3,
    "navbar_color_style": "is-white",  # see styles: https://bulma.io/documentation/components/navbar/#colors
    "logo": {"text": "Bulma Sphinx Theme", "logo": "_static/logo.svg"},
    "header_icons": [
        {
            "name": "Github",
            "url": "https://github.com/zclab/bulma-sphinx-theme",
            "image": "https://www.svgrepo.com/show/433505/github-o.svg",
        },
        {
            "name": "Bulma",
            "url": "https://bulma.io/",
            "image": "https://bulma.io/favicons/favicon.ico",
        },
        {
            "name": "Pydata",
            "url": "https://pydata-sphinx-theme.readthedocs.io/en/latest/",
            "image": "https://pydata-sphinx-theme.readthedocs.io/en/latest/_static/pydata-logo.png",
        },
    ],
    "external_links": [
        {"name": "Furo", "url": "https://pradyunsg.me/furo/quickstart/"},
        {
            "name": "Sphinx book theme",
            "url": "https://sphinx-book-theme.readthedocs.io/en/latest/",
        },
        {
            "name": "Hugging Face community",
            "url": "https://huggingface.co/docs/transformers/index",
        },
        {
            "name": " Docusaurus",
            "url": "https://docusaurus.io/",
        },
    ],
    "source_repository": "https://github.com/zclab/bulma-sphinx-theme",
    "source_branch": "main",
    "source_directory": "docs/",
    "use_edit_page_button": True,
    "fix_navbar": True,
    "navbar_start": [],
    "navbar_end": ["navbar-nav.html", "header-icons.html"],
    "have_top_navbar": True,
}

import hashlib
import logging
import os
import sphinx.application
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import get_translation
from . import pygment, toctree, transforms, utils

__version__ = "0.1.0.dev2"
logger = logging.getLogger(__name__)
MESSAGE_CATALOG_NAME = "bulmasphinxtheme"


def _get_html_theme_path():
    """Return list of HTML theme paths."""
    parent = Path(__file__).parent.resolve()
    theme_path = parent / "theme" / "bulma_sphinx_theme"
    return theme_path


@lru_cache(maxsize=None)
def _asset_hash(path: str) -> str:
    """Append a `?digest=` to an url based on the file content."""
    full_path = _get_html_theme_path() / "static" / path
    digest = hashlib.sha1(full_path.read_bytes()).hexdigest()

    return f"_static/{path}?digest={digest}"


def _add_asset_hashes(static: List[str], add_digest_to: List[str]) -> None:
    for asset in add_digest_to:
        index = static.index("_static/" + asset)
        static[index].filename = _asset_hash(asset)  # type: ignore


def _html_page_context(
    app: sphinx.application.Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: Any,
) -> None:
    assert isinstance(app.builder, StandaloneHTMLBuilder)

    if "css_files" in context:
        _add_asset_hashes(
            context["css_files"],
            ["styles/bulma-sphinx-theme.css"],
        )

    # determine the startdepth for building the theme
    have_navbar = context.get("theme_have_top_navbar", True)
    if not isinstance(have_navbar, bool):
        have_navbar = True
    context["start_depth"] = int(have_navbar)

    # Basic constants
    context["theme_version"] = __version__
    # Translations
    translation = get_translation(MESSAGE_CATALOG_NAME)
    context["translate"] = translation


def _builder_inited(app: sphinx.application.Sphinx) -> None:
    theme_options = utils.get_theme_options(app)

    have_navbar = theme_options.get("have_top_navbar", True)
    if not (have_navbar):
        theme_options["fix_navbar"] = False

    # define navbar style
    default_navbar_directly = ["navbar-nav.html", "icon-links.html"]
    navbar_directly = theme_options.get("navbar_include_directly", None)
    if navbar_directly and isinstance(navbar_directly, list):
        default_navbar_directly.extend(navbar_directly)

    theme_options["navbar_include_directly"] = default_navbar_directly

    # define information panel
    default_panel_items = ["search-button.html"]
    info_panel = theme_options.get("information_panel", {})
    if info_panel.get("items"):
        info_panel["items"] = info_panel.get("items")
    else:
        info_panel["items"] = default_panel_items
    if info_panel.get("level_items"):
        info_panel["level_items"] = info_panel.get("level_items")

    theme_options["information_panel"] = info_panel

    # Prepare the logo config dictionary
    theme_logo = theme_options.get("logo")
    if not theme_logo:
        # In case theme_logo is an empty string
        theme_logo = {}
    if not isinstance(theme_logo, dict):
        raise ValueError(f"Incorrect logo config type: {type(theme_logo)}")
    theme_options["logo"] = theme_logo

    # Add an analytics ID to the site if provided
    analytics = theme_options.get("analytics", {})
    if analytics:
        # Google Analytics
        gid = analytics.get("google_analytics_id")

        if gid:
            gid_js_path = f"https://www.googletagmanager.com/gtag/js?id={gid}"
            gid_script = f"""
                window.dataLayer = window.dataLayer || [];
                function gtag(){{ dataLayer.push(arguments); }}
                gtag('js', new Date());
                gtag('config', '{gid}');
            """

            # Link the JS files
            app.add_js_file(gid_js_path, loading_method="async")
            app.add_js_file(None, body=gid_script)

    def _update_default(key: str, *, new_default: Any) -> None:
        app.config.values[key] = (new_default, *app.config.values[key][1:])

    # Change the default permalinks icon
    _update_default("html_permalinks_icon", new_default="#")


def update_and_remove_templates(
    app: sphinx.application.Sphinx, pagename: str, templatename: str, context, doctree
) -> None:
    template_sections = [
        "theme_navbar_start",
        "theme_navbar_end",
        "theme_navbar_include_directly",
        "theme_article_top_left",
        "theme_article_top_right",
        "theme_article_bottom_left",
        "theme_article_bottom_right",
        "theme_article_footer",
        "theme_footer",
        "sidebars",
    ]

    for section in template_sections:
        if context.get(section):
            # Break apart `,` separated strings so we can use , in the defaults
            if isinstance(context.get(section), str):
                context[section] = [
                    ii.strip() for ii in context.get(section).split(",")
                ]

            # Add `.html` to templates with no suffix
            for ii, template in enumerate(context.get(section)):
                if not os.path.splitext(template)[1]:
                    context[section][ii] = template + ".html"


def setup(app: sphinx.application.Sphinx) -> Dict[str, Any]:
    """Entry point for sphinx theming."""
    app.require_sphinx("3.0")

    theme_dir = _get_html_theme_path()
    app.add_html_theme("bulma_sphinx_theme", theme_dir)
    app.add_post_transform(transforms.ShortenLinkTransform)
    app.add_post_transform(transforms.WrapTableAndMathInAContainerTransform)
    # Translations
    locale_dir = os.path.join(theme_dir, "static", "locales")
    app.add_message_catalog(MESSAGE_CATALOG_NAME, locale_dir)

    app.connect("html-page-context", _html_page_context)
    app.connect("html-page-context", update_and_remove_templates)
    app.connect("html-page-context", toctree.add_toctree_functions)
    app.connect("builder-inited", _builder_inited)
    app.connect("build-finished", pygment.overwrite_pygments_css)
    app.config.templates_path.append(str(theme_dir / "components"))

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }

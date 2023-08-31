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

__version__ = "0.2.1"
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
    if sphinx.version_info >= (7, 1):
        # https://github.com/sphinx-doc/sphinx/pull/11415 added the relevant
        # functionality to Sphinx, so we don't need to do anything.
        return

    for asset in add_digest_to:
        index = static.index("_static/" + asset)
        static[index].filename = _asset_hash(asset)  # type: ignore


def _compute_hide_toc(
    context: Dict[str, Any],
    *,
    builder: StandaloneHTMLBuilder,
    docname: str,
) -> bool:
    # Should the table of contents be hidden?
    file_meta = context.get("meta", None) or {}
    if "hide-toc" in file_meta:
        return True
    elif "toc" not in context:
        return True
    elif not context["toc"]:
        return True

    return False


def _compute_hide_tocnav(
    context: Dict[str, Any],
    *,
    builder: StandaloneHTMLBuilder,
    docname: str,
) -> bool:
    # Should the sidenav be hidden?
    file_meta = context.get("meta", None) or {}
    if "hide-tocnav" in file_meta:
        return True

    if "full-width" in file_meta:
        return True

    return False


def _compute_hide_sidenav(
    context: Dict[str, Any],
    *,
    builder: StandaloneHTMLBuilder,
    docname: str,
) -> bool:
    # Should the sidenav be hidden?
    file_meta = context.get("meta", None) or {}
    if "hide-sidenav" in file_meta:
        return True

    if "full-width" in file_meta:
        return True

    return False


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

    context["hide_toc"] = _compute_hide_toc(
        context, builder=app.builder, docname=pagename
    )
    context["hide_tocnav"] = _compute_hide_tocnav(
        context, builder=app.builder, docname=pagename
    )
    context["hide_sidenav"] = _compute_hide_sidenav(
        context, builder=app.builder, docname=pagename
    )

    # determine the startdepth for building the theme
    have_navbar = context.get("theme_have_top_navbar")
    context["start_depth"] = int(have_navbar)

    # Basic constants
    context["theme_version"] = __version__
    # Translations
    translation = get_translation(MESSAGE_CATALOG_NAME)
    context["translate"] = translation


def _builder_inited(app: sphinx.application.Sphinx) -> None:
    theme_options = utils.get_theme_options(app)

    have_navbar = theme_options.get("have_top_navbar", True)
    if not isinstance(have_navbar, bool):
        raise ValueError(f"Incorrect have_top_navbar config type: {type(have_navbar)}")
    if not (have_navbar):
        theme_options["fix_navbar"] = False

    theme_options["have_top_navbar"] = have_navbar

    # define navbar style
    default_wrapped_navbar = [
        "search-button.html",
        "search-icon.html",
        "search-field.html",
        "theme-swither.html",
    ]
    navbar_wrapped = theme_options.get("navbar_wrapped_items", None)
    if navbar_wrapped and isinstance(navbar_wrapped, list):
        default_wrapped_navbar.extend(navbar_wrapped)
    theme_options["navbar_wrapped_items"] = default_wrapped_navbar

    # define sidenav panel
    default_panel_items = ["search-button.html"]
    require_wrapped_panel_items = ["theme-swither.html", "icon-links.html"]
    sidenav_panel = theme_options.get("sidenav_panel")
    sidenav_panel_wrapped_items = theme_options.get("sidenav_panel_wrapped_items", [])

    if sidenav_panel is None:
        sidenav_panel = default_panel_items
    if not isinstance(sidenav_panel, list):
        raise ValueError(f"Incorrect sidenav_panel config type: {type(sidenav_panel)}")
    if not isinstance(sidenav_panel_wrapped_items, list):
        raise ValueError(
            f"Incorrect sidenav_panel_wrapped_items config type: {type(sidenav_panel_wrapped_items)}"
        )

    sidenav_panel.extend(sidenav_panel_wrapped_items)
    sidenav_panel_set = list(set(sidenav_panel))
    sidenav_panel_set.sort(key=sidenav_panel.index)
    require_wrapped_panel_items.extend(sidenav_panel_wrapped_items)

    panel_items, wrapped_panel_items = [], []
    for item in sidenav_panel_set:
        if item in require_wrapped_panel_items:
            wrapped_panel_items.append(item)
        else:
            panel_items.append(item)
    theme_options["sidenav_panel"] = panel_items
    theme_options["sidenav_panel_wrapped_items"] = wrapped_panel_items

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
        "theme_navbar_wrapped_items",
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
    app.require_sphinx("6.0")

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

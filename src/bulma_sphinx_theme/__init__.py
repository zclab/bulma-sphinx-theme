import hashlib
import logging
import sphinx.application
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List
from sphinx.builders.html import StandaloneHTMLBuilder
from ._toctree import add_toctree_functions
from ._transforms import ShortenLinkTransform, WrapTableAndMathInAContainerTransform
from .utils import get_theme_options

__version__ = "0.0.0"
logger = logging.getLogger(__name__)


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
    if "scripts" in context:
        _add_asset_hashes(
            context["scripts"],
            ["scripts/bulma-sphinx-theme.js"],
        )

    # Basic constants
    context["theme_version"] = __version__


def _builder_inited(app: sphinx.application.Sphinx) -> None:
    def _update_default(key: str, *, new_default: Any) -> None:
        app.config.values[key] = (new_default, *app.config.values[key][1:])

    # Change the default permalinks icon
    _update_default("html_permalinks_icon", new_default="#")


def _update_config(app: sphinx.application.Sphinx) -> None:
    get_theme_options(app)


def setup(app: sphinx.application.Sphinx) -> Dict[str, Any]:
    """Entry point for sphinx theming."""
    app.require_sphinx("3.0")

    theme_dir = _get_html_theme_path()
    app.add_html_theme("bulma_sphinx_theme", theme_dir)
    app.add_post_transform(ShortenLinkTransform)
    app.add_post_transform(WrapTableAndMathInAContainerTransform)

    app.connect("html-page-context", _html_page_context)
    app.connect("html-page-context", add_toctree_functions)
    app.connect("builder-inited", _builder_inited)
    app.connect("builder-inited", _update_config)
    app.config.templates_path.append(str(theme_dir / "components"))

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }

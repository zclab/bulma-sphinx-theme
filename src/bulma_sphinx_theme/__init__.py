import logging
import sphinx.application
from typing import Any, Dict


__version__ = "0.0.0"
logger = logging.getLogger(__name__)


def setup(app: sphinx.application.Sphinx) -> Dict[str, Any]:
    """Entry point for sphinx theming."""
    app.require_sphinx("3.0")

from sphinx.application import Sphinx
from typing import Iterator
from docutils.nodes import Node


def config_provided_by_user(app: Sphinx, key: str) -> bool:
    """Check if the user has manually provided the config.
    This is from pydata sphinx theme.
    """
    return any(key in ii for ii in [app.config.overrides, app.config._raw_config])


def get_theme_options(app: Sphinx):
    """Return theme options for the application w/ a fallback if they don't exist.
    In general we want to modify app.builder.theme_options if it exists, so prefer that first.
    """
    if hasattr(app.builder, "theme_options"):
        # In most HTML build cases this will exist except for some circumstances (see below).
        return app.builder.theme_options
    elif hasattr(app.config, "html_theme_options"):
        # For example, linkcheck will have this configured but won't be in builder obj.
        return app.config.html_theme_options
    else:
        # Empty dictionary as a fail-safe.
        return {}


def activate_extensions(app: Sphinx, extensions):
    """Activate extensions bundled with this theme.

    This also manually triggers the `config-inited` build step to account for
    added extensions that hook into this event.
    """

    # Remove all of the `config-inited` event listeners because they've already triggered
    # We'll then re-trigger this event after adding extensions so that *only* their event hooks trigger
    old_listeners = app.events.listeners["config-inited"]
    app.events.listeners["config-inited"] = []

    for extension in extensions:
        # If it's already been activated just skip it
        if extension in app.config.extensions:
            continue
        app.setup_extension(extension)

    # Emit the config-inited event so that the new extensions run their hooks
    app.emit("config-inited", app.config)

    # Finally join back the lists
    app.events.listeners["config-inited"][:0] = old_listeners


def traverse_or_findall(node: Node, condition: str, **kwargs) -> Iterator[Node]:
    """Triage node.traverse (docutils <0.18.1) vs node.findall.

    TODO: This check can be removed when the minimum supported docutils version
    for numpydoc is docutils>=0.18.1.
    """
    return (
        node.findall(condition, **kwargs)
        if hasattr(node, "findall")
        else node.traverse(condition, **kwargs)
    )

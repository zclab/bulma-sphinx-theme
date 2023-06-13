# Search button

By default, the search input field is hidden, and there is a search button (`search-button.html`) at the sidenav panel, as shown in this site. The search input field will be displayed when a user either:

- Clicks the search button at the sidenav panel.
- Presses the keyboard shortcut {kbd}`Ctrl` + {kbd}`K` (Linux, Windows) or {kbd}`⌘` + {kbd}`K` (macOS).

You can aslo place search icon (`search-icon.html`) in the navbar or sidenav to only display the icon (which does not have search bar text around it).

## Configure the search bar text

To modify the text that is in the search bar before people click on it, add the
following configuration to your `conf.py` file:

```py
html_theme_options = {
    "search_bar_text": "Your text here..."
}
```

# Changing Fonts

The default body and code fonts can be changed Using Custom configuration, you can specify which fonts to use for body or code in `conf.py`. For example, the following configuration can be used to change body and code fonts:

```python
html_theme_options = {
    "css_variables": {
        "font-stack": "Georgia, LXGWWenKaiLite",
        "font-stack--monospace": "monospace"
    },
}
```

If the font you want to specify is not generally available by default, you will additionally need to ensure the font is loaded. For example, you could download and vendor the font in the \_static directory of your Sphinx site and using custom css to define the font as follows,

```css
@font-face {
  font-family: LXGWWenKaiLite;
  font-weight: 300;
  font-style: normal;
  font-display: swap;
  src: url(./LxgwWenKai-Lite/LXGWWenKaiLite-Light.ttf) format(truetype);
}
```

Then, add custom stylesheet as introduced at [Adding custom CSS Stylesheets](./styling.md).

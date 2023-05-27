# Navbar configuration

## Changing the navbar color style

The navbar color style can be changed using the following configuration, see [Bulma Navbar Colors](https://bulma.io/documentation/components/navbar/#colors) for more information,

```python
html_theme_options = {
    "navbar_color_style": "is-white"
}
```

## Fix navbar

The navbar will be hidded when scrolling, to make navbar fixed when scrolling, using the following configuration,

```python
html_theme_options = {
    "fix_navbar": True,
}
```

## Disable navbar

You can also disable navbar using the following configuration, the apperance will be like [Furo](https://pradyunsg.me/furo/quickstart/).

```python
html_theme_options = {
    "have_top_navbar": False
}
```

```{note}
When you disable navbar, fix navbar will not work even you set `fix_navbar` to `True`.
```

## Changing header icons

Bulma sphinx theme allows customising the icons that are presented in the header. These icons can be used to link to relevant resources for your project and documentation. To add custom header icons, you need to provide the `header_icons` configuration value as follows,

```python
html_theme_options = {
    "header_icons": [
        {"name":"Gitlab", "url": "http://gitlabcom/zclab/bulma-sphinx-theme", "fontawesome":"fa-brands fa-lg fa-gitlab"},
    ],
}
```

````{note}
If you wish to use Font Awesome icons, Using `html_css_files` to add the CSS file(s) for Font Awesome.
```python
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]
```
````

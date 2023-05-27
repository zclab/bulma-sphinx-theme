# Changing sidenav elements

Bulma sphinx theme supports customising the elements that show up in the sidenav (left).

## Changing sidenav width

Bulma sphinx theme allows specifying the width of sidenav, the sidenav width is `20%` by default. To change the width, you need to provide the `sidenav-width` css variable configuration value to Bulma sphinx theme, for example,

```python
html_theme_options = {
    "css_variables": {
        "sidenav-width": "20%",
    }
}
```

# Changing sidenav elements

Bulma sphinx theme supports customising the elements that show up in the sidenav (left).

## Changing sidenav width

Bulma sphinx theme allows specifying the width of sidenav, the sidenav width is `20%` by default. To change the width, you need to provide the `sidenav-width` css variable configuration value to Bulma sphinx theme, for example,

```python
html_theme_options = {
    "css_variables": {
        "sidenav-width": "320px",
    }
}
```

## Changing sidenav background

We can also specify the sidenav background (light color or dark color). To change the background, you need to provide the `bst-color-background-sidenav` color variable value to Bulma sphinx theme, for example,

```python
html_theme_options = {
    "light_colors": {
        "bst-color-background-sidenav": "rgb(240, 248, 255)",
    },
    "dark_colors": {
        "bst-color-background-sidenav": "black",
    },
}
```

```{note}
Bulma sphinx theme does not check the value of the color variable, make sure you provide the right value to make it work!
```

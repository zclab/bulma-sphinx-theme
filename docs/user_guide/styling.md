# Adding custom CSS Stylesheets

You may customize the theme’s CSS by creating a custom stylesheet that Sphinx uses to build your site. Any rules in this style-sheet will over-ride the default theme rules. To add a custom stylesheet, follow these steps:

1. **Create a CSS stylesheet** in `_static/css/custom.css`, and add the CSS rules you wish.
2. **Attach the stylesheet to your Sphinx build**. Add the following to `conf.py`
   ```python
   html_static_path = ['_static']
   html_css_files = [
       'css/custom.css',
   ]
   ```

When you build your documentation, this stylesheet should now be activated.

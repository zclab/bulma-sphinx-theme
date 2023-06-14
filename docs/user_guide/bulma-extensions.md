# Using bulma extensions

We do not integrate [bulma extensions](https://bulma.io/extensions/) in this theme. If you want to use these extensions in your page, the following steps are required:

1. add required css following [Adding custom CSS Stylesheets](./styling.md).
2. add required js in `conf.py`, see [html_js_files](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_js_files).
3. using `raw` directive in your markdown or rst files
   ````
   ```{raw} html
   ```
   ````

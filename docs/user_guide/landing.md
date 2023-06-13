# Changing landing page

It is possible to have a custom landing page in Sphinx documentation. This is achieved by adding a custom template file for that page and setting [`html_additional_pages`][additional-pages] in `conf.py`.

```py
templates_path = ["_templates"]
html_additional_pages = {
    "index": "your-custom-landing-page.html"
}
```

```{note}
You'll need to write HTML for the page in `_templates/your-custom-landing-page.html`, if you use the above example as-is. Meanwhile, set `master_doc` configuration or `root_doc` configuration in `conf.py` to `content` or other file name for documentation root page. See [Demo](https://zclab.github.io/bst-demo/) for example.
```

[additional-pages]: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_additional_pages

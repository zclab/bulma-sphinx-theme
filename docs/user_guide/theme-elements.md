# Theme-specific elements

This page elements is from [pydata theme](https://pydata-sphinx-theme.readthedocs.io/en/latest/user_guide/theme-elements.html) to test the styles of bulma sphinx theme.

```{contents} Page contents
:local:
```

## Mathematics

Most Sphinx sites support math, but it is particularly important for scientific computing and so we illustrate support here as well.

Here is an inline equation: {math}`X_{0:5} = (X_0, X_1, X_2, X_3, X_4)` and {math}`another` and {math}`x^2 x^3 x^4` another. And here's one to test vertical height {math}`\frac{\partial^2 f}{\partial \phi^2}`.

Here is block-level equation:

```{math}
:label: My label

\nabla^2 f =
\frac{1}{r^2} \frac{\partial}{\partial r}
\left( r^2 \frac{\partial f}{\partial r} \right) +
\frac{1}{r^2 \sin \theta} \frac{\partial f}{\partial \theta}
\left( \sin \theta \, \frac{\partial f}{\partial \theta} \right) +
\frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2}
```

And here is a really long equation with a label!

```{math}
:label: My label 2

\nabla^2 f =
\frac{1}{r^2} \frac{\partial}{\partial r}
\left( r^2 \frac{\partial f}{\partial r} \right) +
\frac{1}{r^2 \sin \theta} \frac{\partial f}{\partial \theta}
\left( \sin \theta \, \frac{\partial f}{\partial \theta} \right) +
\frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2}
\nabla^2 f =
\frac{1}{r^2} \frac{\partial}{\partial r}
\left( r^2 \frac{\partial f}{\partial r} \right) +
\frac{1}{r^2 \sin \theta} \frac{\partial f}{\partial \theta}
\left( \sin \theta \, \frac{\partial f}{\partial \theta} \right) +
\frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2}
```

And here is a multi-line equation with a label!

```{math}
:label: My label 3

\begin{array}{l}
G_{13}=0 \\
G_{12}=r_{13}+\gamma G_{13}=-1+0.6 \times 0=-1 \\
G_{11}=r_{12}+\gamma G_{12}=-1+0.6 \times(-1)=-1.6 \\
G_{10}=r_{11}+\gamma G_{11}=-1+0.6 \times(-1.6)=-1.96 \\
G_{9}=r_{10}+\gamma G_{10}=-1+0.6 \times(-1.96)=-2.176 \approx-2.18 \\
G_{8}=r_{9}+\gamma G_{9}=-1+0.6 \times(-2.176)=-2.3056 \approx-2.3 \\
\end{array}
```

You can add a link to equations like the one above: {eq}`My label` and {eq}`My label 2` and {eq}`My label 3`.

## Code blocks

Code block styling is inspired by [GitHub's code block style](https://primer.style/css/components/markdown) and also has support for Code Block captions/titles.
See [the Sphinx documentation on code blocks](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block) for more information.

```python
print("A regular code block")
print("A regular code block")
print("A regular code block")
```

You can also provide captions with code blocks, which will be displayed just above the code.
For example, the following code:

````md
```{code-block} python
:caption: python.py

print("A code block with a caption.")
```
````

results in:

```{code-block} python
:caption: python.py

print("A code block with a caption.")
```

You can also display line numbers.
For example, the following code:

````md
```{code-block} python
:caption: python.py
:linenos:

print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
```
````

results in:

```{code-block} python
:caption: python.py
:linenos:

print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
```

## Inline code

When used directly, the `code` role just displays the text without syntax highlighting, as a literal. As mentioned in the [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#inline-code-highlighting) you can also enable syntax highlighting by defining a custom role. It will then use the same highligther as in the `code-block` directive.

```{code-block} rst

.. role:: python(code)
   :language: python

In Python you can :python:`import sphinx`.
```

```{role} python(code)
:language: python
```

In Python you can {python}`import sphinx`.

## Admonition sidebars

```{admonition} A sidebar admonition!
:class: sidebar note
I was made with the `{admonition}` directive and a `sidebar` class.
```

```{sidebar} Sidebar title
I was made with the `{sidebar}` directive.
```

## Footnotes

Here's one footnote[^1] and another footnote [^2] and a named footenote[^named], symbol [^*].

[^1]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.
[^2]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.
[^named]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.
[^*]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.

## Version changes

This theme supports a short-hand way of making **admonitions behave like sidebars**.
This can be a helpful way of highlighting content that lives to the side of your main text without interrupting the vertical flow as much.

For example, look to the right of an "admonition sidebar" and a traditional Sphinx sidebar.

To make an admonition behave like a sidebar, add the `sidebar` class to its list of classes.
For example, the admonition sidebar was created with the following markdown:

````md
```{admonition} A sidebar admonition!
:class: sidebar note
Some sidebar content.
```
````

## Link shortening for git repository services

For example (Please visit [pydata theme](https://pydata-sphinx-theme.readthedocs.io/en/latest/user_guide/theme-elements.html#link-shortening-for-git-repository-services) for more information.):

- **MyST Markdown (default)**

  - `[https://github.com/pydata/pydata-sphinx-theme/pull/1012](https://github.com/pydata/pydata-sphinx-theme/pull/1012)`
  - [https://github.com/pydata/pydata-sphinx-theme/pull/1012](https://github.com/pydata/pydata-sphinx-theme/pull/1012)

# Develop this theme

This page describes the tooling used during development of this theme. It also serves as a reference for the various commands that you would use when working on this theme.

## Overview

The codebase contains Python code, Jinja2-based HTML pages, Sass stylesheets, Scss stylesheets and Javascript code. The following tools are used in developing the theme:

- [nox](https://nox.readthedocs.io/en/stable/) is used for automating development tasks.
- [Webpack-based](https://webpack.js.org/) build pipeline is used to process the Sass, Scss and Javascript files.
- [sphinx-autobuild](https://github.com/executablebooks/sphinx-autobuild) is used to provide live-reloading pages when working on the theme.
- [pre-commit](https://pre-commit.com/) is used for running the linters.

## Theme structure

This theme follows the [`sphinx-theme-builder` filesystem layout](https://sphinx-theme-builder.readthedocs.io/en/latest/filesystem-layout/).

## Initial Setup

To work on this project, you need to have git 2.17+ and Python 3.7+. You also need to be on a platform that is officially supported by NodeJS 18.

1. Clone this project using git:

   ```bash
   git clone https://github.com/zclab/bulma-sphinx-theme.git
   cd bulma-sphinx-theme
   ```

2. Install the project’s development workflow runner:

   ```bash
   pip install nox
   ```

3. Install `pre-commit`, `pre-commit` allows us to run several checks on the codebase every time a new Git commit is made, install it with the following command :

   ```bash
   pip install pre-commit
   ```

   then navigate to this repository’s folder and activate it like so:

   ```bash
   pre-commit install
   ```

   This will install the necessary dependencies to run `pre-commit` every time you make a commit with Git.

With the above step, you’re all set for working on this project.

## Build the theme

Now that you have `nox` installed and cloned the repository, you should be able to build the documentation locally.

### Local Development Server

The following command serve this project’s documentation locally, using [`sphinx-autobuild`](https://github.com/executablebooks/sphinx-autobuild). This will open the generated documentation page in your browser.

```bash
nox -s docs-live
```

The server also watches for changes made to the documentation (`docs/`) or theme (`src/`), which will trigger a **rebuild**. Once the build is completed, server will automagically reload any open pages using livereload.

### Generate Documentation

The following commands generates the documentation into the build/docs folder. This (mostly) does the same thing as `nox -s docs-live`, except it invokes `sphinx-build` instead of `sphinx-autobuild`.

```
nox -s docs
```

### Code Linting

Run the linters, as configured with [pre-commit](https://pre-commit.com/).

```bash
nox -s lint
```

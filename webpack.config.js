const { resolve } = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const dedent = require("dedent");
const { Compilation } = require("webpack");

// Compile our translation files
const { exec } = require("child_process");
exec("python src/bulma_sphinx_theme/_translations.py");

const scriptPath = resolve(__dirname, "src/bulma_sphinx_theme/assets/scripts");
const stylePath = resolve(__dirname, "src/bulma_sphinx_theme/assets/styles");
const staticPath = resolve(__dirname, "src/bulma_sphinx_theme/theme/bulma_sphinx_theme/static");
const vendorPath = resolve(staticPath, "vendor");

/*******************************************************************************
 * functions to load the assets in the html head
 * the css, and js (preload/scripts) are digested for cache busting
 * the fonts are loaded from vendors
 */

function stylesheet(css) { return `<link href="{{ pathto('_static/${css}', 1) }}?digest=${this.hash}" rel="stylesheet" />`; }
function preload(js) { return `<link rel="preload" as="script" href="{{ pathto('_static/${js}', 1) }}?digest=${this.hash}" />`; }
function script(js) { return `<script src="{{ pathto('_static/${js}', 1) }}?digest=${this.hash}"></script>`; }
function font(woff2) { return `<link rel="preload" as="font" type="font/woff2" crossorigin href="{{ pathto('_static/${woff2}', 1) }}" />`; }


/*******************************************************************************
 * the assets to load in the macro
 */
const theme_scripts = [
  "scripts/bulma-sphinx-theme.js",
];

function macroTemplate({ compilation }) {

  return dedent(`\
        <!--
            AUTO-GENERATED from webpack.config.js, do **NOT** edit by hand.
            These are re-used in layout.html
        -->
        {% macro head_js_preload() %}
        <!-- Pre-loaded scripts that we'll load fully later -->
        ${theme_scripts.map(preload.bind(compilation)).join("\n")}
        {% endmacro %}

        {% macro body_post() %}
        <!-- Scripts loaded after <body> so the DOM is not blocked -->
        ${theme_scripts.map(script.bind(compilation)).join("\n")}
        {% endmacro %}
    `);
}

const htmlWebpackPlugin = new HtmlWebpackPlugin({
  filename: resolve(staticPath, "webpack-macros.html"),
  inject: false,
  minify: false,
  css: true,
  templateContent: macroTemplate,
});
/*******************************************************************************/

module.exports = {
  mode: "production",
  devtool: "source-map",
  entry: {
    "bulma-sphinx-theme": [
      resolve(scriptPath, "bulma-sphinx-theme.js"),
      resolve(stylePath, "bulma-sphinx-theme.sass"),
    ],
  },
  output: { filename: "scripts/[name].js", path: staticPath },
  plugins: [new MiniCssExtractPlugin({ filename: "styles/[name].css" }), htmlWebpackPlugin],
  optimization: { minimizer: [`...`, new CssMinimizerPlugin()] },
  module: {
    rules: [{
      test: /\.s[ac]ss$/i,
      use: [
        MiniCssExtractPlugin.loader,
        { loader: "css-loader", options: { url: false, } },
        { loader: "postcss-loader", options: { sourceMap: true } },
        {
          loader: "sass-loader", options: {
            sourceMap: true,
            implementation: require("sass"),
            sassOptions: { outputStyle: "expanded" }
          }
        },
      ],
    }],
  },
};

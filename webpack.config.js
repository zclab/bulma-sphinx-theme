const { resolve } = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const dedent = require("dedent");
const { Compilation } = require("webpack");

const scriptPath = resolve(__dirname, "src/bulma_sphinx_theme/assets/scripts");
const stylePath = resolve(__dirname, "src/bulma_sphinx_theme/assets/styles");
const staticPath = resolve(__dirname, "src/bulma_sphinx_theme/theme/bulma_sphinx_theme/static");
const vendorPath = resolve(staticPath, "vendor");

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
  plugins: [new MiniCssExtractPlugin({ filename: "styles/[name].css" }), htmlWebpackPlugin, copyPlugin],
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

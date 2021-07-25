const path = require("path")
module.exports = {
    entry: {
        index: './src/index.js',
        ckeditor_icons: './src/ckeditor-icons.js',
        tagin: './src/tagin.js',
      },
    mode: 'development',
    output: {
        path: path.resolve(__dirname, '../assets/js'),
        filename: "[name].js",
    },
};

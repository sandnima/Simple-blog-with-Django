const path = require("path")
module.exports = {
    entry: {
        "bootstrap": './src/js/bootstrap.js',
        "ckeditor-icons": './src/js/ckeditor-icons.js',
        "tagin": './src/js/tagin.js',
      },
    mode: 'development',
    output: {
        path: path.resolve(__dirname, '../assets/js'),
        filename: "[name].js",
    },
    module: {
        rules: [
            {
                test: /\.(scss)$/,
                use: ['style-loader', 'css-loader', 'sass-loader']
            },
            {
                test: /\.(css)$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    }
};

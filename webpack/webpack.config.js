const path = require("path")
module.exports = {
    entry: {
        "bootstrap": './src/js/bootstrap.js',
        "ckeditor": './src/js/ckeditor.js',
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
                test: /\.js$/,
                include: path.resolve(__dirname, "node_modules/@ckeditor"),
                use: [{
                    loader: 'babel-loader',
                }]
            },
            {
                test: /\.(scss)$/,
                use: ['style-loader', 'css-loader', 'sass-loader']
            },
            {
                test: /\.(css)$/,
                use: ['style-loader', 'css-loader']
            },
            {
              test: /\.svg$/,
              include: path.resolve(__dirname, "node_modules/@ckeditor"),
              use: [ 'raw-loader' ]
            },
        ]
    }
};

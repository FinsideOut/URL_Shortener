// webpack.config.js
const path = require('path');

module.exports = {
    mode: 'development', // or 'production'
    entry: './URL_Shortener/static/script.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, './URL_Shortener/static/dist')
    },
};
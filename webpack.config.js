var config = {
    entry: {
        bundle: './artcase_proj/core/src/core/base.jsx'
    },
    devtool: 'source-map',
    output: {
        path: './artcase_proj/core/static/core/',
        filename: '[name].js'
    },
    module: {
        loaders: [
            {
                test: /\.jsx$/,
                loader: 'babel-loader',
                query: {
                    presets: ['es2015', 'react']
                }
            },
            {
                test: /\.scss$/,
                loaders: [ 'style', 'css?sourceMap', 'sass?sourceMap' ]
            }
        ]
    },
    externals: {
        //don't bundle libraries but get from CDN
        'react': 'React',
        'react-dom': 'ReactDOM',
        'd3': 'd3'
    },
    // plugins: {
    //     new webpack.ProvidePlugin({
    //         d3: 'd3'
    //     })
    // }
    resolve: {
        // require('file') instead of require('file.js')
        extensions: ['', '.js', '.jsx', '.json', '.css', '.scss']
    }
}

module.exports = config
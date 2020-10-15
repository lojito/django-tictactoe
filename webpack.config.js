module.exports = {
  entry:'./game/static/game/board.js',

  module:{
    rules:[
    {
      test: /\.js$/,
      exclude: /(node_modules)/,
      loader: 'babel-loader',
      options: {
        presets: ['@babel/preset-env',
                 {
                  'plugins': ['@babel/plugin-proposal-class-properties']
                }]
      }
    }]
  },
  
  output: {
    path: __dirname + '/game/static/game',
    filename: 'bundle.js'
  }
  
}




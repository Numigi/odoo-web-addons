
module.exports = {  
  entry: "./main.js",
  mode: "production",
  output: {filename: "webContextualSearchFavorite.js"},
  module: {
    rules: [
      {test: /\.js$/, loader: 'babel-loader'}
    ]
  }
};

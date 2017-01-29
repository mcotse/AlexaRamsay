var request = require('request')
options = { uri: 'http://54.90.201.24:5000/recipe',
  method: 'POST',
  json: { ingredients: [ 'rice', 'chicken' ] } }
request(options, function(err, res, body){
  console.log(body);
})

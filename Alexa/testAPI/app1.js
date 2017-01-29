var request = require('request')

request('http://54.90.201.24:5000/recipe', function(err, res, body){
  console.log(body)
})

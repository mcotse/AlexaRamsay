const express = require('express')
const app = express()
const bodyParser = require('body-parser')

app.use(bodyParser.json());

let exampleRecipeRes = {
  "recipe_name": "chicken alfredo"
}

let exampleStepRes = {
  "instruction": "boil the pasta for six minutes"
}


app.get('/recipe', function (req, res) {
  res.json(exampleRecipeRes)
})

app.get('/step', function (req, res) {

  res.json(exampleStepRes)
})

app.post('/ingr', function (req, res) {
  console.log(req.body);
  res.json(exampleRecipeRes);
})

app.listen(3333, function () {
  console.log('Example app listening on port 3333!')
})

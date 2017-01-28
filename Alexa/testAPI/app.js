const express = require('express')
const app = express()

let exampleRecipeRes = {
  "name": "chicken alfredo"
}

let exampleStepRes = {
  "step": "boil the pasta for six minutes"
}


app.get('/get_next_recipe', function (req, res) {
  res.json(exampleRecipeRes)
})

app.get('/get_next_step', function (req, res) {

  res.json(exampleStepRes)
})

app.listen(3333, function () {
  console.log('Example app listening on port 3333!')
})

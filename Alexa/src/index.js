var Alexa = require('alexa-sdk');
var request = require('request');

var url = process.env.uri;
var handlers = {

    "LaunchRequest": function () {
      var speechOutput = "Welcome to Ramsay. I can guide you through recipes based on your dietitians perscription";
      this.emit(':ask',speechOutput);
    },
    'Unhandled': function() {
      this.emit(':ask', 'Nooooooo we have a problem');
    },
    "NextRecipeIntent": function () {
      var self = this;
      request(url + "/recipe", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          var cardTitle = 'Recipe Name';
          var cardContent = body.recipe_name;
          var speechOutput = 'would you like to make ' + body.recipe_name;
          self.emit(':askWithCard', speechOutput, cardTitle, cardContent)
        } else {
          self.emit(':tell', 'I could not find a recipe, please try again');
        }
      });
    },
    "CurrentRecipeIntent": function () {
      var self = this;
      request(url + "/current_recipe", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          var cardTitle = 'Recipe Name';
          var cardContent = body.recipe_name;
          var speechOutput = 'the current recipe is ' + body.recipe_name;
          self.emit(':tellWithCard', speechOutput, cardTitle, cardContent)
        } else {
          self.emit(':tell', 'I could not find the current recipe, please try again');
        }
      });
    },
    "NextStepIntent": function () {
      var self = this;
      request(url + "/step", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          var cardTitle = 'Step procedure';
          var cardContent = body.instruction;
          var speechOutput = body.instruction;
          self.emit(':tellWithCard', speechOutput, cardTitle, cardContent)
        }
      });
    },
    "LastStepIntent": function () {
      var self = this;
      request(url + "/previous_step", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          var cardTitle = 'Step procedure';
          var cardContent = body.instruction;
          var speechOutput = body.instruction;
          self.emit(':tellWithCard', speechOutput, cardTitle, cardContent)
        }
      });
    },
    "StartOverStepIntent": function () {
      var self = this;
      request(url + "/current_recipe", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          var cardTitle = 'Recipe Name';
          var recipeName = body.recipe_name;
          request(url + "/first_step", function(err, res, body){
            if (!err && res.statusCode == 200){
              console.log('hi');
              body = JSON.parse(body);
              var cardContent = body.instruction;
              var speechOutput = 'starting over with the recipe ' + recipeName + '. ' +  body.instruction;
              self.emit(':tellWithCard', speechOutput, cardTitle, cardContent)
            }
          });
        } else {
          self.emit(':tell', 'I could not find the current recipe, please try again');
        }
      });
    },
    "IngredientsToRecipeIntent": function() {
      var self = this;
      var ingredients = this.event.request.intent.slots;
      var ingr_array = [];
      for (var key in ingredients) {
        for (var name in ingredients[key]){
          if (name == 'value'){
            ingr_array.push(ingredients[key][name])
          }
        }
      };
      var options = {
        uri: url + "/recipe",
        method: "POST",
        json: { "ingredients": ingr_array }
      };
      request(options, function(err, res, body){
        if (!err && res.statusCode == 200){
          console.log(body);
          var cardTitle = 'Recipe Name';
          var cardContent = body.recipe_name;
          var speechOutput = 'would you like to make ' + body.recipe_name;
          self.emit(':askWithCard', speechOutput, cardTitle, cardContent)
        } else {
          self.emit(':ask', 'I could not find a recipe, try again with different ingredients');
        }
      })
    },
  //   { i_two: { name: 'i_two', value: 'rice' },
  // i_one: { name: 'i_one', value: 'chicken' },
  // i_three: { name: 'i_three' },
  // i_four: { name: 'i_four' } }
    "AMAZON.YesIntent": function () {
      this.emit('NextStepIntent');
    },
    "AMAZON.NoIntent": function () {
      this.emit('NextRecipeIntent');
    }
};

exports.handler = function(event, context, callback) {
    var alexa = Alexa.handler(event, context);
    alexa.appId = process.env.app_id;
    alexa.registerHandlers(handlers);
    alexa.execute();
};

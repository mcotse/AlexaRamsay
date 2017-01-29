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
      var userId = this.event.session.user.userId.replace('amzn1.ask.account.','');
      var options = {
        uri: url + "/recipe",
        method: "GET",
        qs: {userId}
      };
      request(options, function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          var cardTitle = 'Recipe Name';
          var cardContent = body.recipe_name;
          var speechOutput = 'would you like to make ' + body.recipe_name;
          var repromptSpeech = 'would you like to make ' + body.recipe_name;
          console.log(body);
          // if ('img_url' in body){
          //   if (body.img_url.indexOf('.jpg') !== -1){
          //     var index = body.img_url.lastIndexOf(".jpg");
          //     var img_url = body.img_url.substring(0, index + 4);
          //     var imageObj = {
          //       smallImageUrl: img_url,
          //       largeImageUrl: img_url
          //     }
          //     console.log('1');
          //     self.emit(':askWithCard', speechOutput, repromptSpeech, cardTitle, cardContent, imageObj);
          //   }
          //
          //   // self.emit(':AskWithCard', speechOutput, cardTitle, cardContent, imageObj);
          // } else {
          //   console.log('2');
          // }
          console.log(speechOutput, cardTitle, cardContent);
          self.emit(':askWithCard', speechOutput, cardTitle, cardContent);
        } else {
          self.emit(':tell', 'I could not find a recipe, please try again');
        }
      });
    },
    "CurrentRecipeIntent": function () {
      var self = this;
      var userId = this.event.session.user.userId.replace('amzn1.ask.account.','');
      var options = {
        uri: url + "/current_recipe",
        method: "GET",
        qs: {userId}
      };
      request(options, function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          var cardTitle = 'Recipe Name';
          var cardContent = body.recipe_name;
          var speechOutput = 'the current recipe is ' + body.recipe_name;
          if ('img_url' in body){
            var imageObj = {
              smallImageUrl: body.img_url,
              largeImageUrl: body.img_url
            };
            self.emit(':tellWithCard', speechOutput, cardTitle, cardContent, imageObj);
          } else {
            self.emit(':tellWithCard', speechOutput, cardTitle, cardContent);
          }
        } else {
          self.emit(':tell', 'I could not find the current recipe, please try again');
        }
      });
    },
    "NextStepIntent": function () {
      var self = this;
      var userId = this.event.session.user.userId.replace('amzn1.ask.account.','');
      var options = {
        uri: url + "/step",
        method: "GET",
        qs: {userId}
      };
      request(options, function(err, res, body){
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
      var userId = this.event.session.user.userId.replace('amzn1.ask.account.','');
      var options = {
        uri: url + "/previous_step",
        method: "GET",
        qs: {userId}
      };
      request(options, function(err, res, body){
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
      var userId = this.event.session.user.userId.replace('amzn1.ask.account.','');
      var options = {
        uri: url + "/current_recipe",
        method: "GET",
        qs: {userId}
      };
      request(options, function(err, res, body){
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
      var userId = this.event.session.user.userId.replace('amzn1.ask.account.','');
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
        json: { "ingredients": ingr_array },
        qs: {userId}
      };
      console.log(options);
      request(options, function(err, res, body){
        if (!err && res.statusCode == 200){
          console.log(body);
          var cardTitle = 'Recipe Name';
          var cardContent = body.recipe_name;
          var speechOutput = 'would you like to make ' + body.recipe_name;
          if ('img_url' in body){
            var imageObj = {
              smallImageUrl: body.img_url,
              largeImageUrl: body.img_url
            };
            self.emit(':tellWithCard', speechOutput, cardTitle, cardContent, imageObj);
          } else {
            self.emit(':tellWithCard', speechOutput, cardTitle, cardContent);
          }
        } else {
          self.emit(':ask', 'I could not find a recipe, try again with different ingredients');
        }
      })
    },
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

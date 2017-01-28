var request = require('request');
/**
 * App ID for the skill
 */
var APP_ID = process.env.app_id; //replace with "amzn1.echo-sdk-ams.app.[your-unique-value-here]";

/**
 * The AlexaSkill prototype and helper functions
 */
var AlexaSkill = require('./AlexaSkill');

var Ramsey = function () {
    AlexaSkill.call(this, APP_ID);
};

// Extend AlexaSkill
Ramsey.prototype = Object.create(AlexaSkill.prototype);
Ramsey.prototype.constructor = Ramsey;

Ramsey.prototype.eventHandlers.onSessionStarted = function (sessionStartedRequest, session) {
    console.log("Ramsey onSessionStarted requestId: " + sessionStartedRequest.requestId
        + ", sessionId: " + session.sessionId);
    // any initialization logic goes here
};

Ramsey.prototype.eventHandlers.onLaunch = function (launchRequest, session, response) {
    console.log("Ramsey onLaunch requestId: " + launchRequest.requestId + ", sessionId: " + session.sessionId);
    var speechOutput = "Welcome to Ramsey. I can guide you through recipes based on your dietitians perscription";
    var repromptText = "ask for a recipe";
    response.ask(speechOutput, repromptText);
};

Ramsey.prototype.eventHandlers.onSessionEnded = function (sessionEndedRequest, session) {
    console.log("Ramsey onSessionEnded requestId: " + sessionEndedRequest.requestId
        + ", sessionId: " + session.sessionId);
    // any cleanup logic goes here
};

Ramsey.prototype.intentHandlers = {
    // register custom intent handlers
    "GetNextRecipe": function (intent, session, response) {
      request(process.env.uri + "/get_next_recipe", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body)
          dishName = body.name
          response.ask(dishName);
          response.tellWithCard(dishName);
        }
      });
        // var names = [];
        // for (var name in intent.slots){
        //     if("value" in intent.slots[name]){
        //         names.push(intent.slots[name].value);
        //     }
        // }
        // if (names.length == 0){
        //     response.ask("There were no names given, ask again","Ask again")
        // }
        // var randomIndex = Math.floor(Math.random() * names.length)
        // response.tellWithCard(names[randomIndex]);
    },
    "GetNextStep": function (intent, session, response) {
      request(process.env.uri + "/get_next_recipe", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body)
          response.ask(body.name);
          response.tellWithCard(body.name);
        }
      });
        // var min, max;
        // if("value" in intent.slots.Num_one && "value" in intent.slots.Num_two){
        //     min = Math.min(intent.slots.Num_one.value,intent.slots.Num_two.value);
        //     max = Math.max(intent.slots.Num_one.value,intent.slots.Num_two.value);
        // }else{
        //     response.ask("I cant work with what you just gave me, try asking again with another range","Ask again")
        // }
        // //generate random number in the given range
        // var randomNum = Math.floor(Math.random()*(max-min+1))+min;
        // response.tellWithCard(randomNum.toString());
    },
    "AMAZON.HelpIntent": function (intent, session, response) {
        response.ask("Ask for next steps or next recipe");
    }
};

// Create the handler that responds to the Alexa Request.
exports.handler = function (event, context) {
    // Create an instance of the Ramsey skill.
    var ramsey = new Ramsey();
    ramsey.execute(event, context);
};

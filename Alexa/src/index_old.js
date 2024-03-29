'use strict';
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
    var speechOutput = "Welcome to Ramsay. I can guide you through recipes based on your dietitians perscription";
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
      request(process.env.uri + "/recipe", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          response.ask('would you like to make ' + body.recipe_name);
          response.tellWithCard(body.recipe_name);
          return;
        }
      });
    },
    "GetNextStep": function (intent, session, response) {
      request(process.env.uri + "/step", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          response.ask(body.instruction);
          response.tellWithCard(body.instruction);
          return;
        }
      });
    },
    // "GetNextStep": function (intent, session, response) {
    //   request(process.env.uri + "/step", function(err, res, body){
    //     if (!err && res.statusCode == 200){
    //       body = JSON.parse(body);
    //       response.ask(body.instruction);
    //       response.tellWithCard(body.instruction);
    //       return;
    //     }
    //   });
    },
    "AMAZON.HelpIntent": function (intent, session, response) {
        response.ask("Ask for next steps or next recipe");
    },
    "AMAZON.YesIntent": function (intent, session, response) {
      request(process.env.uri + "/recipe", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          response.ask(body.recipe_name);
          response.tellWithCard(body.recipe_name);
          return;
        }
      });
    },
    "AMAZON.NoIntent": function (intent, session, response) {
      request(process.env.uri + "/step", function(err, res, body){
        if (!err && res.statusCode == 200){
          body = JSON.parse(body);
          response.ask('would you like to make ' + body.instruction);
          response.tellWithCard(body.instruction);
          return;
        }
      });
    }
};

// Create the handler that responds to the Alexa Request.
exports.handler = function (event, context) {
    // Create an instance of the Ramsey skill.
    var ramsey = new Ramsey();
    ramsey.execute(event, context);
};

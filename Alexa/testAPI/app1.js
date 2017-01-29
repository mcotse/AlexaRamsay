var request = require('request')
var url = 'http://52.23.225.246'
var userId = 'AGGMIF4XQRD3F2TCQVJWZ47RU7PQNUL4MDFDNFN6WI5OJ5UZMJT52QQ7CSBJLDHBUVDZK6CPO7F5W2YI6PUDESC454Y3PZCKMEZSJEBBZ3SXBJQ7WR6YJYUSUPXKTBQM6WNPRQJEP3FIANG5OQ3G4MQFKPKU75PXIBCVCAROZ6KXNS7YPPSEIV36O3O6Z37OLFL5ZADFDFXGFRY'
var options = {
  uri: url + "/recipe",
  method: "GET",
  qs: {userId}
};
request(options, function(err, res, body){
  body = JSON.parse(body)
  console.log(body.recipe_name)
  // console.log(body.img _url)
  if ('img_url' in body){
    if (body.img_url.indexOf('.jpg') !== -1){
      var index = body.img_url.lastIndexOf(".jpg");
      var img_url = body.img_url.substring(0, index + 4);
      console.log(img_url)
    }
  }
})

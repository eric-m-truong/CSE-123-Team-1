//
//var debugButton = document.getElementsByClassName("debugBox")[0];
//var debugButton = buttonArray[0];

//debugButton.onclick = function() {debugEvent()};
var dict = new Object();
var listOfIds = [];





// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  for (var key in dict) {
    client.subscribe("plux/control/" + key);
    console.log("Subscribed to: " + "plux/control/" + key);
  }
  //client.subscribe("MQTTPS");
  //message = new Paho.MQTT.Message("Hello");
  //message.destinationName = "World";
  //client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  //console.log("onMessageArrived:"+message.payloadString);
  console.log(message.payloadString + message.destinationName);
  if (parseInt(message.payloadString) == 0 || parseInt(message.payloadString) == 1) {
    dict[message.destinationName] = parseInt(message.payloadString);
    //console.log(message.destinationName + message.payloadString + "hi");
  }
}

function getAllPlugs() {
  var elements = document.getElementsByName("statusSignal");
  for (var i = 0, j = elements.length; i < j; i++) {
    //console.log(elements[i].getAttribute('id'));
    listOfIds.push(elements[i].getAttribute('id'));
    dict[elements[i].getAttribute('id')] = 0;
  }
}


function sendSignal() {
  //console.log(debugButton);
  var buttonStatus = document.getElementsByName("statusSignal");
  //console.log(buttonStatus[0].getAttribute('id'));
  //console.log(buttonStatus[1].getAttribute('id'));
  //console.log(buttonStatus[2].getAttribute('id'));
  //console.log(buttonStatus[3].getAttribute('id'));
  //console.log(listOfIds.length);

  for (var i = 0, j = listOfIds.length; i < j; i++) {
    for (var key in dict) {
      //console.log(key + " and " + i);


      if (key === (buttonStatus[i].getAttribute('id'))) {
        if (dict[key] == 0 && buttonStatus[i].checked == true) {
          dict[key] = 1;
          message = new Paho.MQTT.Message("1");
          message.retained = true;
          message.destinationName = "plux/control/" + key;
          client.send(message);
          return;
        }
        else if (dict[key] == 1 && buttonStatus[i].checked == false) {
          dict[key] = 0;
          message = new Paho.MQTT.Message("0");
          message.retained = true;
          message.destinationName = "plux/control/" + key;
          client.send(message);
          return;
        }
        /*else if (dict[key] == 0 && buttonStatus[i].checked == false) {
          message = new Paho.MQTT.Message("0");
          message.retained = true;
          message.destinationName = key;
          client.send(message);
          return;
        }
        else if (dict[key] == 1 && buttonStatus[i].checked == true) {
          message = new Paho.MQTT.Message("1");
          message.retained = true;
          message.destinationName = key;
          client.send(message);
          return;
        }*/

      }
    }
  }
  /*if (buttonStatus[0].checked === true) {
    //console.log("On!");
    message = new Paho.MQTT.Message("1");
    message.retained = true;
    message.destinationName = "MQTTPS";
    client.send(message);
  }
  else if (buttonStatus[0].checked === false) {
    message = new Paho.MQTT.Message("0");
    message.retained = true;
    message.destinationName = "MQTTPS";
    client.send(message);
  }*/
  //console.log(buttonStatus);
  //document.getElementsByClassName("checkbox")[0].checked;


  //console.log(2);
}

console.log("Don't mind me.\n");
window.onload = getAllPlugs();
client = new Paho.MQTT.Client("mosquitto.projectplux.info", Number(15676), "clientId1234");
// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({ userName: "eric", password: "truong", useSSL: true, onSuccess: onConnect });
const pluxSignal = document.querySelectorAll('input[type="checkbox"]')
for (var X = 0, Y = pluxSignal.length; X < Y; X++) {
  pluxSignal[X].addEventListener('click', sendSignal);
}


// get all the checkboxes on the page
//var checkboxes = document.querySelectorAll('input[type=checkbox]');

// add a change event listener
//for(var i = 0; i < checkboxes.length; i++) {
//    checkboxes[i].addEventListener('change', function(){
//        console.log('the checkbox changed' + i);
//    });
//}

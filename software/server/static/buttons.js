//
//var debugButton = document.getElementsByClassName("debugBox")[0];
//var debugButton = buttonArray[0];

//debugButton.onclick = function() {debugEvent()};
var dict = new Object();
var listOfIds = [];
console.log("Don't mind me. 80\n");
window.onload = getAllPlugs();

function getAllPlugs() {
  var elements = document.getElementsByName("statusSignal");
  //console.log(elements);
  for (var i = 0, j = elements.length; i < j; i++) {
    //console.log(elements[i].getAttribute('id'));
    listOfIds.push(elements[i].getAttribute('id'));
    dict[elements[i].getAttribute('id')] = 2;
  }
  //console.log(dict)
}


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  for (var key in dict) {
    client.subscribe("plux/control/ack/" + key);
    console.log("Subscribed to: " + "plux/control/ack/" + key);
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
  //console.log(message.payloadString + " + " + message.destinationName.slice(17));
  if (parseInt(message.payloadString[0]) == 1 || parseInt(message.payloadString[0]) == 2) {
    if (dict[message.destinationName.slice(17)] != parseInt(message.payloadString[0])) {
      //console.log(dict[message.destinationName.slice(17)] + " plus " + message.destinationName.slice(17))
      if (parseInt(message.payloadString[0]) == 1) {
        //console.log(document.getElementById(message.destinationName.slice(17)).checked)
        document.getElementById(message.destinationName.slice(17)).checked = true;
        //console.log("on!")
      }
      if (parseInt(message.payloadString[0]) == 2) {
        //console.log(document.getElementById(message.destinationName.slice(17)).checked)
        document.getElementById(message.destinationName.slice(17)).checked = false;
        //console.log("off!")
      }
    }
    dict[message.destinationName.slice(17)] = parseInt(message.payloadString[0]);
    //console.log(message.destinationName.slice(17) + " and " + message.payloadString + " and hi");
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
      //console.log(listOfIds[i])
      //console.log(key + " and " + i);


      if (key === (buttonStatus[i].getAttribute('id'))) {
        if (dict[key] == 2 && buttonStatus[i].checked == true) {
          dict[key] = 1;
          message = new Paho.MQTT.Message("1");
          message.retained = true;
          message.destinationName = "plux/control/" + key;
          client.send(message);
          //console.log("Let's go!1")
          return;
        }
        else if (dict[key] == 1 && buttonStatus[i].checked == false) {
          dict[key] = 2;
          message = new Paho.MQTT.Message("2");
          message.retained = true;
          message.destinationName = "plux/control/" + key;
          client.send(message);
          //console.log("Oh no!2")
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


client = new Paho.MQTT.Client("mosquitto.projectplux.info", Number(80), "clientId1234");
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

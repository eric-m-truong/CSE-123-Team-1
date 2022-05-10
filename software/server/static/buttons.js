//
//var debugButton = document.getElementsByClassName("debugBox")[0];
//var debugButton = buttonArray[0];

//debugButton.onclick = function() {debugEvent()};
var OFF = 0;
var ON = 1;
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
    dict[elements[i].getAttribute('id')] = OFF;
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
  if (parseInt(message.payloadString[0]) == ON || parseInt(message.payloadString[0]) == OFF) {
    if (dict[message.destinationName.slice(17)] != parseInt(message.payloadString[0])) {
      //console.log(dict[message.destinationName.slice(17)] + " plus " + message.destinationName.slice(17))
      if (parseInt(message.payloadString[0]) == ON) {
        //console.log(document.getElementById(message.destinationName.slice(17)).checked)
        document.getElementById(message.destinationName.slice(17)).checked = true;
        //console.log("on!")
      }
      if (parseInt(message.payloadString[0]) == OFF) {
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
        if (dict[key] == OFF && buttonStatus[i].checked == true) {
          dict[key] = ON;
          message = new Paho.MQTT.Message("1");
          message.retained = true;
          message.destinationName = "plux/control/" + key;
          client.send(message);
          console.log(key)
          return;
        }
        else if (dict[key] == ON && buttonStatus[i].checked == false) {
          dict[key] = OFF;
          message = new Paho.MQTT.Message("0");
          message.retained = true;
          message.destinationName = "plux/control/" + key;
          client.send(message);
          console.log(key)
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

var rBuf = new Int8Array(4);
window.crypto.getRandomValues(rBuf);
const r = new DataView(rBuf.buffer).getUint32();

console.log(ip, port, username, password, useSSL)

client = new Paho.MQTT.Client(ip, Number(port), "plux-ctrl" + r);

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({
    onSuccess: onConnect,
    userName: username,
    password: password,
    useSSL: useSSL,
});

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

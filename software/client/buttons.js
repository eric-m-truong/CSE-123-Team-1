//
//var debugButton = document.getElementsByClassName("debugBox")[0];
//var debugButton = buttonArray[0];

//debugButton.onclick = function() {debugEvent()};
client = new Paho.MQTT.Client("mosquitto.projectplux.info", Number(443), "clientId1234");
var options = {
 //   timeout: 5000,
//    hosts: '',
//    ports: 8080,
//    path: '/mqtt'
    useSSL: false
};
// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({userName:"eric",password:"truong", useSSL:true, onSuccess:onConnect});


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("MQTTPS");
  message = new Paho.MQTT.Message("Hello");
  message.destinationName = "World";
  client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  //console.log("onMessageArrived:"+message.payloadString);
  console.log(message.payloadString);
}


function debugEvent() {
    //console.log(debugButton);
    var buttonStatus = document.getElementById("debugBox").checked;
    if (buttonStatus === true) {
        //console.log("On!");
        message = new Paho.MQTT.Message("Hello from JavaScript");
        message.destinationName = "MQTTPS";
        client.send(message);
    }
    //console.log(buttonStatus);
    //document.getElementsByClassName("checkbox")[0].checked;
    
    
    //console.log(2);
}



const betterDebug2 = document.querySelector('input[type="checkbox"]')
betterDebug2.addEventListener('click', debugEvent)
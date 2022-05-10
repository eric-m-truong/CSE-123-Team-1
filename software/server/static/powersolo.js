// create a data source to hold data
const source = new Bokeh.ColumnDataSource({
    data: { x: [], y: [] }
});

// make a plot with some tools
const plot = Bokeh.Plotting.figure({
    x_axis_type: 'datetime',
    sizing_mode: 'stretch_both',
    x_axis_label: 't',
    y_axis_label: 'W',
    tools: 'save',
});

// plot.x_range.flipped = true;

// add a line with data from the source
plot.line({ field: "x" }, { field: "y" }, {
    source: source,
});

// change 443 to 8883 if localhost


// Create a div element
const fakeEle = document.createElement('div');

// Hide it completely
fakeEle.style.position = 'absolute';
fakeEle.style.top = '0';
fakeEle.style.left = '-9999px';
fakeEle.style.overflow = 'hidden';
fakeEle.style.visibility = 'hidden';
fakeEle.style.whiteSpace = 'nowrap';
fakeEle.style.height = '0';

// We copy some styles from the textbox that effect the width
const textboxEle = document.getElementById('dynamicBox');
if (textboxEle.getAttribute('value') == '') {
    textboxEle.setAttribute('value', document.getElementById('hiddenMac').getAttribute('value'))
}

// Get the styles
const styles = window.getComputedStyle(textboxEle);

// Copy font styles from the textbox
fakeEle.style.fontFamily = styles.fontFamily;
fakeEle.style.fontSize = styles.fontSize;
fakeEle.style.fontStyle = styles.fontStyle;
fakeEle.style.fontWeight = styles.fontWeight;
fakeEle.style.letterSpacing = styles.letterSpacing;
fakeEle.style.textTransform = styles.textTransform;

fakeEle.style.borderLeftWidth = styles.borderLeftWidth;
fakeEle.style.borderRightWidth = styles.borderRightWidth;
fakeEle.style.paddingLeft = styles.paddingLeft;
fakeEle.style.paddingRight = styles.paddingRight;

// Append the fake element to `body`
document.body.appendChild(fakeEle);

const setWidth = function () {
    const string = textboxEle.value || textboxEle.getAttribute('placeholder') || '';
    fakeEle.innerHTML = string.replace(/\s/g, '&' + 'nbsp;');

    const fakeEleStyles = window.getComputedStyle(fakeEle);
    textboxEle.style.width = fakeEleStyles.width;
};

setWidth();

textboxEle.addEventListener('input', function (e) {
    setWidth();
});



plot.outline_line_color = null;
plot.toolbar.logo = null;
plot.toolbar_location = null;
plot.outline_line_alpha = 0;
plot.border_fill_alpha = 0;
var doc = new Bokeh.Document()
doc.add_root(plot)
var div = document.getElementById("BokehPlot")
Bokeh.embed.add_document_standalone(doc, div);



var dict = new Object();
var listOfIds = [];
var OFF = 0;
var ON = 1;
console.log("No need to worry!\n");

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








function onMessageArrived(message) {
    //console.log("new data " + message.destinationName)
    //console.log()
    if (message.destinationName == ("plux/data/" + mac_addr)) {
        //console.log("ok")
        console.log(message.payloadString + message.destinationName)
        let [ts, pwr] = message.payloadString.split(",").map(parseFloat);
        source.data.x.push(ts);
        source.data.y.push(pwr);
        source.change.emit();
    }
    else if (message.destinationName == ("plux/control/ack/" + mac_addr)) {
        //console.log("lets go")
        //console.log(message.payloadString + message.destinationName)
        if (parseInt(message.payloadString[0]) == ON || parseInt(message.payloadString[0]) == OFF) {
            if (dict[message.destinationName.slice(17)] != parseInt(message.payloadString[0])) {
                if (parseInt(message.payloadString[0]) == ON) {
                    document.getElementById(message.destinationName.slice(17)).checked = true;
                }
                if (parseInt(message.payloadString[0]) == OFF) {
                    document.getElementById(message.destinationName.slice(17)).checked = false;
                }
            }
            dict[message.destinationName.slice(17)] = parseInt(message.payloadString[0]);
            //console.log(message.destinationName.slice(17) + " and " + message.payloadString + " and hi");
        }
    }
}







// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
    }
}




function sendSignal() {
    var buttonStatus = document.getElementsByName("statusSignal");

    for (var i = 0, j = listOfIds.length; i < j; i++) {
        for (var key in dict) {
            if (key === (buttonStatus[i].getAttribute('id'))) {
                if (dict[key] == OFF && buttonStatus[i].checked == true) {
                    dict[key] = ON;
                    message = new Paho.MQTT.Message("1");
                    message.retained = true;
                    message.destinationName = "plux/control/" + mac_addr;
                    client.send(message);
                    //console.log("Let's go!1")
                    return;
                }
                else if (dict[key] == ON && buttonStatus[i].checked == false) {
                    dict[key] = OFF;
                    message = new Paho.MQTT.Message("0");
                    message.retained = true;
                    message.destinationName = "plux/control/" + mac_addr;
                    client.send(message);
                    //console.log("Oh no!2")
                    return;
                }
            }
        }
    }
}

var rBuf = new Int8Array(4);
window.crypto.getRandomValues(rBuf);
const r = new DataView(rBuf.buffer).getUint32();
var mac_addr = document.getElementById('hiddenMac').getAttribute('value');

client = new Paho.MQTT.Client(ip, Number(port), "ws-stream-" + r);
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;


client.connect({
    onSuccess: onConnect,
    userName: username,
    password: password,
    useSSL: useSSL,
});

// called when the client connects
function onConnect() {
    client.subscribe("plux/data/" + mac_addr);
    client.subscribe("plux/control/ack/" + mac_addr);
    console.log("Subscribed to: " + "plux/data/" + mac_addr)
    console.log("Subscribed to: " + "plux/control/ack/" + mac_addr);
}

const pluxSignal = document.querySelectorAll('input[type="checkbox"]')
for (var X = 0, Y = pluxSignal.length; X < Y; X++) {
    pluxSignal[X].addEventListener('click', sendSignal);
}

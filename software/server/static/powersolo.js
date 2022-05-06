// create a data source to hold data
const source = new Bokeh.ColumnDataSource({
    data: { x: [], y: [] }
});

// make a plot with some tools
const plot = Bokeh.Plotting.figure({
    sizing_mode: 'stretch_width',
    x_axis_type: 'datetime',
});

plot.x_range.flipped = true;

// add a line with data from the source
plot.line({ field: "x" }, { field: "y" }, {
    source: source,
});

var rBuf = new Int8Array(4);
window.crypto.getRandomValues(rBuf);
const r = new DataView(rBuf.buffer).getUint32();

// change 443 to 8883 if localhost
client = new Paho.MQTT.Client(ip, Number(80), "ws-stream-" + r);
client.onMessageArrived = onMessageArrived;
client.connect({
    onSuccess: onConnect,
    // comment these out when using localhost
    userName: username,
    password: password,
    useSSL: true,
    // --------------------------------------
});

function onConnect() {
    client.subscribe("plux/data/"+plug_name);
    console.log("Yeah! " + plug_name)
}

function onMessageArrived(m) {
    let [ts, pwr] = m.payloadString.split(",").map(parseFloat);
    source.data.x.push(ts);
    source.data.y.push(pwr);
    source.change.emit();
}

//Bokeh.Plotting.show(plot);

plot.outline_line_color = null;
plot.toolbar.logo = null;
plot.toolbar_location = null;
plot.sizing_mode='stretch_both';
//plot.background_fill_alpha = 0;
plot.outline_line_alpha = 0;
plot.border_fill_alpha = 0;
var doc = new Bokeh.Document()
doc.add_root(plot)
var div = document.getElementById("BokehPlot")
Bokeh.embed.add_document_standalone(doc, div);

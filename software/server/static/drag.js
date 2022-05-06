// Make the DIV element draggable:

//objectWidth = document.getElementById("PowerBox").offsetWidth;
//console.log("objectWidth: " + objectWidth);
function dragElement(mac) {
  //console.log("Binga!")
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(mac + "header")) {
    // if present, the header is where you move the DIV from:
    document.getElementById(mac + "header").onmousedown = dragMouseDown;
    //console.log("Hi!")
  } else {
    //otherwise, move the DIV from anywhere inside the DIV:
    mac.onmousedown = dragMouseDown;
    //console.log("Oh!")
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    //pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    //pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    //pos4 = e.clientY;
    // set the element's new position:
    //elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    if ((mac.offsetLeft - pos1) < (getWidth() - mac.offsetWidth) && (mac.offsetLeft - pos1 > 0)) {
      //console.log((mac.offsetLeft - pos1) + " vs " + mac.style.left.slice(0, -2) + " vs " + (getWidth() - mac.offsetWidth));
      mac.style.left = (mac.offsetLeft - pos1) + "px";

    }

  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}


function getWidth() {
  if (self.innerWidth) {
    return self.innerWidth;
  }
  else if (document.documentElement && document.documentElement.clientHeight) {
    return document.documentElement.clientWidth;
  }
  else if (document.body) {
    return document.body.clientWidth;
  }
  return 0;
}

function getHeight() {
  return Math.max(
    document.body.scrollHeight,
    document.documentElement.scrollHeight,
    document.body.offsetHeight,
    document.documentElement.offsetHeight,
    document.documentElement.clientHeight
  );
}





//dragElement(document.getElementsByClassName("PowerBox")[0]);
const dragSignal = document.querySelectorAll('label[name="dragBox"]')
//console.log(dragSignal[0].getAttribute('id'))
var dragButton = document.getElementsByName("dragBox");
for (var X = 0, Y = dragSignal.length; X < Y; X++) {
  //dragSignal[X].addEventListener('drag', dragElement(dragSignal[X].getAttribute('id')));
  document.getElementsByClassName("PowerBox")[X].style.left = ((document.getElementsByClassName("PowerBox")[0].offsetWidth + 5) * X) + "px";
  dragElement(document.getElementsByClassName("PowerBox")[X]);
}
  //console.log('Width:  ' +  getWidth() );
  //console.log('Height: ' + getHeight() );
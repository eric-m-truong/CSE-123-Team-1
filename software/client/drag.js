// Make the DIV element draggable:
dragElement(document.getElementById("PowerBox"));
//objectWidth = document.getElementById("PowerBox").offsetWidth;
//console.log("objectWidth: " + objectWidth);
function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id + "header")) {
    // if present, the header is where you move the DIV from:
    document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
    elmnt.onmousedown = dragMouseDown;
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
    if ((elmnt.offsetLeft - pos1) < (getWidth() - elmnt.offsetWidth) && (elmnt.offsetLeft - pos1 > 0)) {
        console.log((elmnt.offsetLeft - pos1) + " vs " + elmnt.style.left.slice(0,-2) + " vs " + (getWidth() - elmnt.offsetWidth));
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
        
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
    else if (document.documentElement && document.documentElement.clientHeight){
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
  
  console.log('Width:  ' +  getWidth() );
  console.log('Height: ' + getHeight() );
var wsUri = "ws://127.0.0.1:8009/";
var output;

var init = function() {
    output = document.getElementById("output");
    testWebSocket();
}

var testWebSocket = function() {
    websocket = new WebSocket(wsUri);
    websocket.onopen = function(evt) { onOpen(evt) };
    websocket.onclose = function(evt) { onClose(evt) };
    websocket.onmessage = function(evt) { onMessage(evt) };
    websocket.onerror = function(evt) { onError(evt) };
}

var onOpen = function(evt) {
    writeToScreen("CONNECTED");
    for (var i = 100 - 1; i >= 0; i--) {
        doSend(`sending content item ${i}`)
    }
}

var onClose = function(evt) {
    writeToScreen("DISCONNECTED");
}

var onMessage = function(evt) {
    writeToScreen('<span style="color: blue;">RESPONSE: ' + evt.data+'</span>');
    websocket.close();
}

var onError = function(evt) {
    writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data);
}

var doSend = function(message) {
    writeToScreen("SENT: " + message);
    websocket.send(message);
}

var writeToScreen = function(message) {
    var pre = document.createElement("p");
    pre.style.wordWrap = "break-word";
    pre.innerHTML = message;
    output.appendChild(pre);
}


window.addEventListener("load", init, false);

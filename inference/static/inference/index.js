var chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws'
);

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var prediction = data['prediction'];
    console.log(prediction);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
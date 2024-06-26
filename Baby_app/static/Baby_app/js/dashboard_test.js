console.log("Dashboard works");

const socket = new WebSocket('ws://' + window.location.host + '/ws/xyz/');
console.log(socket)
socket.onmessage = function(msg){
    console.log('Server:' + msg.data);
};

socket.onopen = function(msg){
    socket.send(JSON.stringify({
        'message': 'Hello from Client',
        'sender': 'Brave'
    }));
};

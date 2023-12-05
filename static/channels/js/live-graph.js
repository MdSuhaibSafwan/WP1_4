var user = "{{ user.username }}";
console.log(user);

var ws_protocol = "ws:";
if (location.protocol == "https:"){
  ws_protocol = "wss:"
};

var ws_url = `${ws_protocol}//${location.host}/message/?username=${user}`;
console.log(ws_url);

const socket = new WebSocket(
  ws_url,
);

socket.onclose = (event) => {
    console.log(event);
  }

socket.onopen = (event) => {
// socket.send("Here's some text that the server is urgently awaiting!");
console.log(event);
};

socket.onmessage = (event) => {
    // socket.send("Here's some text that the server is urgently awaiting!");
    console.log(event);
    };

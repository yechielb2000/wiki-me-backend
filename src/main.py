from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from src.socket.room import ConnectionManager

app = FastAPI()
socket: ConnectionManager = ConnectionManager()

HTML = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(HTML)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await socket.connect(websocket)
    if websocket in socket.active_connections:
        await socket.broadcast(f"{socket.active_connections}")
    try:
        while True:
            data = await websocket.receive_text()
            await socket.send_personal_message(f"You wrote: {data}", websocket)
            await socket.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        socket.disconnect(websocket)
        await socket.broadcast(f"Client #{client_id} left the chat")


@app.websocket_route(path="/ws/{room_id}/{client_id}")
async def websocket_client(webscoket: WebSocket, room_id: str, client_id: str):
    pass

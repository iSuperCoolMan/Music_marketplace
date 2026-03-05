from starlette.websockets import WebSocket


class SupportConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def activate_chat(self, user_id):
        data = {
            "action": "add",
            "id": user_id,
            "name": user_id,
        }

        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except:
                pass

    async def deactivate_chat(self, user_id):
        data = {
            "action": "remove",
            "id": user_id,
            "name": user_id,
        }

        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except:
                pass

    async def send_message(self, chat_id: str, text: str, sender: str, time: str):
        data = {
            "action": "message",
            "id": chat_id,
            "text": text,
            "sender": sender,
            "time": time
        }

        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except:
                pass


support_manager = SupportConnectionManager()
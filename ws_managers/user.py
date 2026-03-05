from starlette.websockets import WebSocket


class UserConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, chat_id: str):
        await websocket.accept()
        self.active_connections[chat_id] = websocket

    async def disconnect(self, chat_id: str):
        self.active_connections.pop(chat_id, None)

    def list_active_users(self) -> list[str]:
        return list(self.active_connections.keys())

    async def send_message(self, chat_id: str, text: str, sender: str, time: str):
        websocket = self.active_connections.get(chat_id)

        if websocket:
            await websocket.send_json({"text": text, "sender": sender, "time": time})


user_manager = UserConnectionManager()
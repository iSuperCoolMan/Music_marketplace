import datetime

from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from db.message import try_create_message
from db.support_chat_session import get_chat_session_by_uuid
from db.user import get_user_by_uuid
from ws_managers.user import user_manager
from ws_managers.support import support_manager
from settings import directories


router = APIRouter()

templates = Jinja2Templates(directory=directories.TEMPLATE_DIRECTORY)


@router.websocket("/ws/support")
async def websocket_endpoint(websocket: WebSocket):
    await support_manager.connect(websocket)

    for session_uuid in user_manager.list_active_users():
        try:
            session = await get_chat_session_by_uuid(session_uuid)

            if session.user_uuid is None:
                name = session.ip
            else:
                user = await get_user_by_uuid(session.user_uuid)
                name = user.username

            await websocket.send_json({
                "action": "add",
                "id": session_uuid,
                "name": name
            })
        except:
            pass  # можно залогировать ошибки

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            session_uuid = data.get("id")

            if action == "message" and session_uuid:
                text = data.get("message")
                datetime_now = datetime.datetime.now()
                formatted_time = datetime_now.strftime("%H:%M:%S")

                if not await try_create_message(
                    text=text, date_time=datetime_now, session_uuid=UUID(session_uuid), from_support=True
                ):
                    return None

                await support_manager.send_message(session_uuid, text, "support", formatted_time)
                await user_manager.send_message(session_uuid, text, "support", formatted_time)

            if action == "remove" and session_uuid:
                # Например, закрываем соединение пользователя и шлём всем поддержку обновление
                await user_manager.disconnect(session_uuid)

                # всем техподдержкам отправить, что чат удален
                for ws in support_manager.active_connections:
                    try:
                        await ws.send_json({
                            "action": "remove",
                            "id": session_uuid,
                        })
                    except:
                        pass

    except WebSocketDisconnect:
        support_manager.disconnect(websocket)

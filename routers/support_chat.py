import datetime

from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Cookie
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import Response

from db.message import try_create_message
from db.support_chat_session import get_chat_session_by_uuid, create_chat_session
from ws_managers.user import user_manager
from ws_managers.support import support_manager
from settings import directories


router = APIRouter()

templates = Jinja2Templates(directory=directories.TEMPLATE_DIRECTORY)


@router.get("/api/session/messages")
async def get_session_messages(session_uuid: str | None = Cookie(default=None)):
    if session_uuid is None:
        return None

    session = await get_chat_session_by_uuid(UUID(session_uuid))

    if session is None:
        return None

    return {"messages": session.messages}


@router.post("/api/session")
async def create_session(request: Request, response: Response):
    session = await create_chat_session(ip=request.client.host)
    response.set_cookie(key="session_uuid", value=str(session.uuid), max_age=3600)

    return {"Message": "Session created, cookie set"}


@router.post("/api/session/refresh")
async def refresh_session(response: Response, session_uuid: str | None = Cookie(default=None)):
    if session_uuid is None:
        raise Exception

    response.set_cookie(key="session_uuid", value=session_uuid, max_age=3600)

    return {"Message": "Session cookie refreshed"}


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    session_uuid = websocket.cookies.get("session_uuid")

    if session_uuid is None:
        print(f"session id is none: {session_uuid}")
        return None

    await user_manager.connect(websocket, session_uuid)
    await support_manager.activate_chat(session_uuid)

    try:
        while True:
            text = await websocket.receive_text()
            datetime_now = datetime.datetime.now()
            formatted_time = datetime_now.strftime("%H:%M:%S")

            if not await try_create_message(
                text=text, date_time=datetime_now, session_uuid=UUID(session_uuid), from_support=False
            ):
                print("cant create message")
                return None

            await user_manager.send_message(session_uuid, text, "user", formatted_time)
            await support_manager.send_message(session_uuid, text, "user", formatted_time)
    except WebSocketDisconnect:
        await user_manager.disconnect(session_uuid)
        await support_manager.deactivate_chat(session_uuid)
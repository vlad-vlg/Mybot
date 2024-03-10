from aiogram.fsm.state import StatesGroup, State


class FSMShowMedia(StatesGroup):
    AcceptDocument = State()
    SendDocument = State()
    AcceptAlbumDocument = State()
    SendAlbum = State()

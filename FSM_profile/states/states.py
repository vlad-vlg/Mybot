from aiogram.fsm.state import StatesGroup, State


class FSMGetProfile(StatesGroup):
    EnterFullName = State()
    EnterAge = State()
    UploadPhoto = State()
    EnterComment = State()

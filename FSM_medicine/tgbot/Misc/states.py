from aiogram.fsm.state import StatesGroup, State


class GetMedicine(StatesGroup):
    EnterAddressAndLocation = State()
    EnterFullName = State()
    EnterPrescription = State()

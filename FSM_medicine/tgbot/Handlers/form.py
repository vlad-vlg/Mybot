from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM_medicine.tgbot.Misc.states import GetMedicine


form_router = Router()


@form_router.message(Command('medicine'))
async def get_medicine(message: Message, bot: Bot, state: FSMContext):
    await message.answer('Введите точный адрес или локацию человека')
    await state.set_state(GetMedicine.EnterAddressAndLocation)


@form_router.message(F.text, GetMedicine.EnterAddressAndLocation)
async def get_medicine_enter_address(message: Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await message.answer('Введите Фамилию, Имя, Отчество человека')
    await state.set_state(GetMedicine.EnterFullName)


@form_router.message(F.location, GetMedicine.EnterAddressAndLocation)
async def get_medicine_enter_location(message: Message, state: FSMContext):
    long = message.location.longitude
    lat = message.location.latitude
    await state.update_data(longitude=long, latitude=lat)
    await message.answer('Введите Фамилию, Имя, Отчество человека')
    await state.set_state(GetMedicine.EnterFullName)


@form_router.message(F.text, GetMedicine.EnterFullName)
async def get_medicine_enter_full_name(message: Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer('Введите название лекарств, дозировку и количество')
    await state.set_state(GetMedicine.EnterPrescription)


@form_router.message(F.text, GetMedicine.EnterPrescription)
async def get_medicine_enter_prescription(message: Message, bot: Bot, state: FSMContext):
    prescription = message.text
    data = await state.get_data()
    address = data.get('address', None)
    long = data.get('longitude', None)
    lat = data.get('latitude', None)
    full_name = data.get('full_name')

    username = f'@{message.from_user.username}' if message.from_user.username else ''
    sender_link = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a> {username}'

    text_format = f'''
Адрес: <b>{address}</b>
Координаты: <b>{long}, {lat}</b>
ФИО: <b>{full_name}</b>

{prescription}
 
Отправитель:{sender_link}
'''
    await message.answer(text_format)
    await bot.send_message(-1001990305479, text_format)
    await message.answer('Ваша заявка принята')
    await state.clear()

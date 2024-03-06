from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, PhotoSize
from FSM_profile.states.states import FSMGetProfile


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Приветствую!\n\n'
        'Чтобы перейти к заполнению анкеты - '
        'отправьте команду /fillform'
    )


@router.message(Command('cancel'), StateFilter(default_state))
async def cmd_cancel_no_state(message: Message):
    await message.answer(
        'Отменять нечего.\n\n'
        'Чтобы перейти к заполнению анкеты - '
        'отправьте команду /fillform'
    )


@router.message(Command('cancel'), ~StateFilter(default_state))
async def cmd_cancel(message: Message, state: FSMContext):
    await message.answer(
        'Действие отменено\n\n'
        'Чтобы снова перейти к заполнению анкеты - '
        'отправьте команду /fillform'
    )
    await state.clear()


@router.message(Command('fillform'), StateFilter(default_state))
async def cmd_fillform(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, введите Ваши Фамилию, Имя, Отчество')
    await state.set_state(FSMGetProfile.EnterFullName)


@router.message(StateFilter(FSMGetProfile.EnterFullName), F.text)
async def cmd_enter_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(
        'Спасибо!\n\n'
        'Теперь введите Ваш возраст'
    )
    await state.set_state(FSMGetProfile.EnterAge)


@router.message(StateFilter(FSMGetProfile.EnterFullName))
async def warning_not_name(message: Message):
    await message.answer(
        'Это не похоже на имя\n\n'
        'Пожалуйста, введите Ваше ФИО\n\n'
        'Если Вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel'
    )


@router.message(StateFilter(FSMGetProfile.EnterAge),
                F.text.isdigit())
async def cmd_enter_age(message: Message, state: FSMContext):
    age = message.text
    if int(age) >= 18:
        if int(age) > 100:
            await message.answer('О, да Вы долгожитель!')
        await state.update_data(age=age)
        await message.answer(
            'Спасибо!\n\nТеперь загрузите, пожалуйста, Ваше фото'
        )
        await state.set_state(FSMGetProfile.UploadPhoto)
    else:
        await message.answer(
            'Вы еще слишком молоды!\n'
            'Обратитесь после достижения совершеннолетия'
        )
        await state.clear()


@router.message(StateFilter(FSMGetProfile.EnterAge))
async def warning_not_age(message: Message):
    await message.answer(
        'Возраст должен быть целым числом\n'
        'Попробуйте еще раз\n\nЕсли Вы хотите прервать '
        'заполнение анкеты - отправьте команду /cancel'
    )


@router.message(StateFilter(FSMGetProfile.UploadPhoto),
                F.photo[-1].as_('largest_photo'))
async def cmd_upload_photo(message: Message,
                           state: FSMContext,
                           largest_photo: PhotoSize):
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )
    await message.answer(
        'Спасибо!\n\nВы можете оставить свой комментарий\n\n'
        'Можно пропустить этот шаг, отправив команду /skip'
    )
    await state.set_state(FSMGetProfile.EnterComment)


@router.message(StateFilter(FSMGetProfile.UploadPhoto))
async def warning_not_photo(message: Message):
    await message.answer(
        'Пожалуйста, на этом шаге отправьте Ваше фото\n\n'
        'Если Вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel'
    )


@router.message(StateFilter(FSMGetProfile.EnterComment), F.text)
async def cmd_enter_comment(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(comment=message.text)

    data = await state.get_data()
    full_name = data.get('full_name')
    age = data.get('age')
    photo_id = data.get('photo_id')
    comment = data.get('comment', None)
    username = f'@{message.from_user.username}' if message.from_user.username else ''
    sender_link = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>   {username}'

    text_answer = f'''
ФИО: <b>{full_name}</b>\n
Возраст: <b>{age}</b>\n
Комментарий: <i>{comment}</i>
'''
    await message.answer('Спасибо! Ваши данные сохранены\n\n')
    await message.answer_photo(
        photo=photo_id,
        caption=text_answer,
    )
    await bot.send_message(-1001990305479,
                           f'{text_answer}\n\n'
                           f'Фото ID: {photo_id}\n\n'
                           f'Отправитель: {sender_link}'
                           )
    await state.clear()


@router.message(Command('skip'), StateFilter(FSMGetProfile.EnterComment))
async def cmd_enter_no_comment(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    full_name = data.get('full_name')
    age = data.get('age')
    photo_id = data.get('photo_id')
    username = f'@{message.from_user.username}' if message.from_user.username else ''
    sender_link = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>   {username}'

    text_answer = f'''
ФИО: <b>{full_name}</b>\n
Возраст: <b>{age}</b>
'''
    await message.answer('Спасибо! Ваши данные сохранены\n\n')
    await message.answer_photo(
        photo=photo_id,
        caption=text_answer,
    )
    await bot.send_message(-1001990305479,
                           f'{text_answer}\n\n'
                           f'Фото ID: {photo_id}\n\n'
                           f'Отправитель: {sender_link}'
                           )
    await state.clear()


@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(
        'Извините, моя твоя не понимать!\n\n'
        'Для начала работы отправьте команду /start'
    )

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, Document
from Media.states.states import FSMShowMedia


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Приветствую!\n\n'
        'Это задание к уроку 7.10 <b>"Медиа"</b>\n'
        'Чтобы перейти к выполнению задания, '
        'отправьте команду /begin'
    )


@router.message(Command('cancel'), StateFilter(default_state))
async def cmd_cancel_no_state(message: Message):
    await message.answer(
        'Отменять нечего.\n\n'
        'Чтобы перейти к выполнению задания, '
        'отправьте команду /begin'
    )


@router.message(Command('cancel'), ~StateFilter(default_state))
async def cmd_cancel(message: Message, state: FSMContext):
    await message.answer(
        'Действие отменено\n\n'
        'Чтобы снова перейти к выполнению задания, '
        'отправьте команду /begin'
    )
    await state.clear()


@router.message(Command('begin'), StateFilter(default_state))
async def accept_document(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте боту любой документ')
    await state.set_state(FSMShowMedia.AcceptDocument)


@router.message(StateFilter(FSMShowMedia.AcceptDocument), F.document.as_('document'))
async def accept_document(message: Message, state: FSMContext, bot: Bot, document: Document):
    doc_id = document.file_id
    doc_filename = document.file_name
    await state.update_data(doc_id=doc_id)
    await message.answer(
        'Спасибо!\n\n'
        'Ваш документ получен: \n'
        f'Файл: <b>{doc_filename}</b>\n'
        f'Document ID: <code>{doc_id}</code>\n\n'
        'Для возврата Вашего документа отправьте команду /documents'
    )
    await bot.download(document, r'./Documents')
    await state.set_state(FSMShowMedia.SendDocument)


@router.message(StateFilter(FSMShowMedia.AcceptDocument))
async def warning_not_document(message: Message):
    await message.answer(
        'Это не похоже на документ\n\n'
        'Пожалуйста, отправьте боту любой документ\n\n'
        'Если Вы хотите прервать выполнение задания, '
        'отправьте команду /cancel'
    )


@router.message(Command('documents'), StateFilter(FSMShowMedia.SendDocument))
async def cmd_send_documents(message: Message, state: FSMContext):
    data = await state.get_data()
    doc_id = data.get('doc_id')
    await message.answer_document(document=doc_id)
    await state.set_state(FSMShowMedia.AcceptDocument)
#
# @router.message(StateFilter(FSMShowMedia.AcceptDocument), F.document.as_('document'))
# async def download_document(message: Message, state: FSMContext, bot: Bot, document: Document):
#     doc_id = document.file_id
#     doc_filename = document.file_name
#     # await state.update_data(doc_id=doc_id)
#     await bot.download(document, destination='Documents')
#     await message.answer(
#         'Спасибо!\n\n'
#         'Ваш документ сохранен \n'
#         f'Файл: <b>{doc_filename}</b>'
#     )
#
# #
# @router.message(StateFilter(FSMGetProfile.EnterAge))
# async def warning_not_age(message: Message):
#     await message.answer(
#         'Возраст должен быть целым числом\n'
#         'Попробуйте еще раз\n\nЕсли Вы хотите прервать '
#         'заполнение анкеты - отправьте команду /cancel'
#     )
#
#
# @router.message(StateFilter(FSMGetProfile.UploadPhoto),
#                 F.photo[-1].as_('largest_photo'))
# async def cmd_upload_photo(message: Message,
#                            state: FSMContext,
#                            largest_photo: PhotoSize):
#     await state.update_data(
#         photo_unique_id=largest_photo.file_unique_id,
#         photo_id=largest_photo.file_id
#     )
#     await message.answer(
#         'Спасибо!\n\nВы можете оставить свой комментарий\n\n'
#         'Можно пропустить этот шаг, отправив команду /skip'
#     )
#     await state.set_state(FSMGetProfile.EnterComment)
#
#
# @router.message(StateFilter(FSMGetProfile.UploadPhoto))
# async def warning_not_photo(message: Message):
#     await message.answer(
#         'Пожалуйста, на этом шаге отправьте Ваше фото\n\n'
#         'Если Вы хотите прервать заполнение анкеты - '
#         'отправьте команду /cancel'
#     )
#
#
# @router.message(StateFilter(FSMGetProfile.EnterComment), F.text)
# async def cmd_enter_comment(message: Message, bot: Bot, state: FSMContext):
#     await state.update_data(comment=message.text)
#
#     data = await state.get_data()
#     full_name = data.get('full_name')
#     age = data.get('age')
#     photo_id = data.get('photo_id')
#     comment = data.get('comment', None)
#     username = f'@{message.from_user.username}' if message.from_user.username else ''
#     sender_link = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>   {username}'
#
#     text_answer = f'''
# ФИО: <b>{full_name}</b>\n
# Возраст: <b>{age}</b>\n
# Комментарий: <i>{comment}</i>
# '''
#     await message.answer('Спасибо! Ваши данные сохранены\n\n')
#     await message.answer_photo(
#         photo=photo_id,
#         caption=text_answer,
#     )
#     await bot.send_message(-1001990305479,
#                            f'{text_answer}\n\n'
#                            f'Фото ID: {photo_id}\n\n'
#                            f'Отправитель: {sender_link}'
#                            )
#     await state.clear()
#
#
# @router.message(Command('skip'), StateFilter(FSMGetProfile.EnterComment))
# async def cmd_enter_no_comment(message: Message, bot: Bot, state: FSMContext):
#     data = await state.get_data()
#     full_name = data.get('full_name')
#     age = data.get('age')
#     photo_id = data.get('photo_id')
#     username = f'@{message.from_user.username}' if message.from_user.username else ''
#     sender_link = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>   {username}'
#
#     text_answer = f'''
# ФИО: <b>{full_name}</b>\n
# Возраст: <b>{age}</b>
# '''
#     await message.answer('Спасибо! Ваши данные сохранены\n\n')
#     await message.answer_photo(
#         photo=photo_id,
#         caption=text_answer,
#     )
#     await bot.send_message(-1001990305479,
#                            f'{text_answer}\n\n'
#                            f'Фото ID: {photo_id}\n\n'
#                            f'Отправитель: {sender_link}'
#                            )
#     await state.clear()
#
#
# @router.message(StateFilter(default_state))
# async def send_echo(message: Message):
#     await message.reply(
#         'Извините, моя твоя не понимать!\n\n'
#         'Для начала работы отправьте команду /start'
#     )

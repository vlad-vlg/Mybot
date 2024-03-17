from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, Document
from aiogram.utils.media_group import MediaGroupBuilder

from Media.states.states import FSMShowMedia

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Приветствую!\n\n'
        'Это задание к уроку 7.10 <b>"Медиа"</b>\n'
        'Чтобы перейти к выполнению задания, '
        'отправьте команду /begin\n'
        'Для работы с альбомами, отправьте команду /album'
    )


@router.message(Command('cancel'), StateFilter(default_state))
async def cmd_cancel_no_state(message: Message):
    await message.answer(
        'Отменять нечего.\n\n'
        'Чтобы перейти к выполнению задания, '
        'отправьте команду /begin\n'
        'Для работы с альбомами, отправьте команду /album'
    )


@router.message(Command('cancel'), ~StateFilter(default_state))
async def cmd_cancel(message: Message, state: FSMContext):
    await message.answer(
        'Действие отменено\n\n'
        'Чтобы снова перейти к выполнению задания, '
        'отправьте команду /begin\n'
        'Для работы с альбомами, отправьте команду /album'
    )
    await state.clear()


@router.message(Command('begin'), StateFilter(default_state))
async def cmd_begin(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте боту любой документ')
    await state.set_state(FSMShowMedia.AcceptDocument)


@router.message(StateFilter(FSMShowMedia.AcceptDocument), F.document.as_('document'))
async def accept_document(message: Message, state: FSMContext, bot: Bot, document: Document):
    #   print(document)
    doc_id = document.file_id
    doc_filename = document.file_name
    await state.update_data(doc_id=doc_id)
    await message.answer(
        'Спасибо!\n\n'
        'Ваш документ получен: \n'
        f'Файл: <b>{doc_filename}</b>\n'
        f'Document ID: \n<code>{doc_id}</code>\n\n'
        'Для отправки следующего документа, отправьте команду /more\n'
        'Для возврата Вашего документа отправьте команду /documents'
    )
    await bot.download(document, f'./Documents/{doc_filename}')
    await state.set_state(FSMShowMedia.SendDocument)


@router.message(Command('more'))
async def cmd_add_document(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте боту следующий документ')
    await state.set_state(FSMShowMedia.AcceptDocument)


@router.message(Command('more_album'))
async def cmd_add_document(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте боту следующий документ')
    await state.set_state(FSMShowMedia.AcceptAlbumDocument)


# @router.message(StateFilter(FSMShowMedia.AcceptDocument))
# @router.message(StateFilter(FSMShowMedia.AcceptAlbumDocument))
# async def warning_not_document(message: Message):
#     await message.answer(
#         'Это не похоже на документ\n\n'
#         'Пожалуйста, отправьте боту любой документ\n\n'
#         'Если Вы хотите прервать выполнение задания, '
#         'отправьте команду /cancel'
#     )


@router.message(Command('documents'), StateFilter(FSMShowMedia.SendDocument))
async def cmd_send_documents(message: Message, state: FSMContext):
    data = await state.get_data()
    doc_id = data.get('doc_id')
    await message.answer_document(document=doc_id)
    await message.answer(
        'Для отправки следующего документа, отправьте команду /more\n'
        'Для возврата Вашего документа отправьте команду /documents'
    )


@router.message(Command('album'), StateFilter(default_state))
async def cmd_album(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте боту любой документ')
    await state.set_state(FSMShowMedia.AcceptAlbumDocument)


@router.message(StateFilter(FSMShowMedia.AcceptAlbumDocument), F.document.as_('document'))
async def accept_album_document(message: Message, state: FSMContext, document: Document):
    print(document)
    doc_id = document.file_id
    doc_filename = document.file_name
    file_id = document.file_unique_id

    files = dict()
    files[file_id] = doc_id
    await state.update_data(files)

    await message.answer(
        'Спасибо!\n\n'
        'Ваш документ получен: \n'
        f'Файл: <b>{doc_filename}</b>\n'
        f'Document ID: \n<code>{doc_id}</code>\n\n'
        'Для отправки следующего документа, отправьте команду /more_album\n'
        'Для получения альбома документов отправьте команду /get_album'
    )
    await state.set_state(FSMShowMedia.SendAlbum)


@router.message(Command('get_album'), StateFilter(FSMShowMedia.SendAlbum))
async def cmd_send_album(message: Message, state: FSMContext):
    data = await state.get_data()
    #    print(data)
    #    album_files = [data[key] for key in data]
    #    print(album_files)
    album_builder = MediaGroupBuilder(caption="Ваш альбом")
    if len(data) <= 10:
        for key in data:
            album_builder.add_document(
                media=data[key]
            )
        await message.answer_media_group(
            media=album_builder.build()
        )
        await message.answer(
            'Для отправки следующего документа, отправьте команду /more_album\n'
            'Для получения альбома документов отправьте команду /get_album'
        )
    else:
        await message.answer(
            'В альбоме не может быть более 10 элементов!\n\n'
            'Для отмены отправьте команду /cancel\n'
            'Для возврата в начало работы отправьте команду /start'
        )

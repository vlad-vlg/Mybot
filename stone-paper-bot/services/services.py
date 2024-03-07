import random

LEXICON_RU: dict[str, str] = {
    'rock': 'Камень 🗿',
    'paper': 'Бумага 📜',
    'scissors': 'Ножницы ✂'
}


def get_bot_choice() -> str:
    return random.choice(['rock', 'paper', 'scissors'])


# Функция, возвращающая ключ из словаря, по которому
# хранится значение, передаваемое как аргумент - выбор пользователя
def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            return key


# Функция, определяющая победителя
def get_winner(user_answer: str, bot_choice: str) -> str:
    user_choice = _normalize_user_answer(user_answer)
    print(bot_choice, user_choice, sep='\n')
    rules = {'rock': 'scissors',
             'scissors': 'paper',
             'paper': 'rock'}
    if user_choice == bot_choice:
        return f'Ничья!\n\nПродолжим?'
    elif rules[user_choice] == bot_choice:
        return f'Ты победил! Поздравляю!\n\nДавай сыграем еще?'
    return f'Я победил!\n\nСыграем еще?'

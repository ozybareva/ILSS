from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu_keyboard():
    kb = [
        [KeyboardButton(text="Расписание на неделю")],
        [KeyboardButton(text="Задание на день")],
        [KeyboardButton(text="Комментарии к недельному плану")],
        [KeyboardButton(text="Результаты тренировок и комментарии тренера")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )


def get_week_info():
    kb = [
        [KeyboardButton(text="Текущая неделя")],
        [KeyboardButton(text="Выбрать неделю")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )


def get_day_info():
    kb = [
        [KeyboardButton(text="Сегодня")],
        [KeyboardButton(text="Выбрать день")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

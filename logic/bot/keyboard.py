from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ButtonText:
    BUTTON_SCHEDULE_TEXT = 'Расписание на неделю'
    BUTTON_TASK_TEXT = 'Задание на день'
    BUTTON_COMMENT_TEXT = 'Комментарии к недельному плану'
    BUTTON_TRAIN_RESULTS_TEXT = 'Результаты тренировок и комментарии тренера'
    BUTTON_CURRENT_WEEK_SCHEDULE_TEXT = 'Получить расписание на текущую неделю'
    BUTTON_CURRENT_DAY_TEXT = 'Получить задание на сегодня'
    BUTTON_SELECT_DATE = 'Выбрать дату'
    BUTTON_MAIN_MENU = 'Вернуться в основное меню'


def get_menu_keyboard():
    kb = [
        [KeyboardButton(text=ButtonText.BUTTON_CURRENT_WEEK_SCHEDULE_TEXT)],
        [KeyboardButton(text=ButtonText.BUTTON_CURRENT_DAY_TEXT)],
        [KeyboardButton(text=ButtonText.BUTTON_SELECT_DATE)],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )


def get_options_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text=ButtonText.BUTTON_SCHEDULE_TEXT),
           KeyboardButton(text=ButtonText.BUTTON_TASK_TEXT))
    kb.add(KeyboardButton(text=ButtonText.BUTTON_COMMENT_TEXT),
           KeyboardButton(text=ButtonText.BUTTON_TRAIN_RESULTS_TEXT))

    kb.add(KeyboardButton(text=ButtonText.BUTTON_MAIN_MENU))

    return kb

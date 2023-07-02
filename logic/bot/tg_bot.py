from aiogram import Bot, Dispatcher, types
from telegram_bot_calendar import DetailedTelegramCalendar

from logic.bot.keyboard import get_menu_keyboard
from persistance.repository import Repository
from settings import Settings

LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}

class ILSSBot:
    def __init__(self, settings: Settings, repository: Repository):
        self.bot = Bot(token=settings.api_token)
        self.dp = Dispatcher(self.bot)
        self.repository = repository
        self.register_handlers()

    def register_handlers(self):
        self.dp.register_message_handler(self.start, commands=["start"])
        self.dp.register_message_handler(self.send_schedule, text=["Расписание на неделю"])
        self.dp.register_message_handler(self.send_task, text=["Задание на день"])
        self.dp.register_message_handler(self.send_comment, text=["Комментарии к недельному плану"])
        self.dp.register_message_handler(self.send_train_results, text=["Результаты тренировок и комментарии тренера"])
        self.dp.register_callback_query_handler(self.task_cal)
        self.dp.register_callback_query_handler(self.schedule_cal)
        self.dp.register_callback_query_handler(self.comment_cal)
        self.dp.register_callback_query_handler(self.train_results_cal)

    async def start(self, message: types.Message):
        keyboard = get_menu_keyboard()
        await message.answer('Выберите опцию', reply_markup=keyboard)

    async def send_message(self, chat_id: str, message: str):
        return await self.bot.send_message(chat_id=chat_id, text=message)

    async def send_task(self, message: types.Message):
        await self.select_task_date(message)

    async def send_schedule(self, message: types.Message):
        await self.select_schedule_week(message)

    async def send_comment(self, message: types.Message):
        await self.select_comment_week(message)

    async def send_train_results(self, message: types.Message):
        await self.select_train_result_week(message)

    async def select_task_date(self, message: types.Message):
        calendar, step = WYearTelegramCalendar(calendar_id=1, locale='ru').build()
        await self.bot.send_message(message.chat.id,
                                    f'Выбрать {LSTEP[step]}',
                                    reply_markup=calendar)

    async def select_schedule_week(self, message: types.Message):
        calendar, step = DetailedTelegramCalendar(calendar_id=2, locale='ru').build()
        await self.bot.send_message(message.chat.id,
                                    f'Выбрать {LSTEP[step]}',
                                    reply_markup=calendar)

    async def select_comment_week(self, message: types.Message):
        calendar, step = DetailedTelegramCalendar(calendar_id=3, locale='ru').build()
        await self.bot.send_message(message.chat.id,
                                    f'Выбрать {LSTEP[step]}',
                                    reply_markup=calendar)

    async def select_train_result_week(self, message: types.Message):
        calendar, step = DetailedTelegramCalendar(calendar_id=4, locale='ru').build()
        await self.bot.send_message(message.chat.id,
                                    f"Выбрать {LSTEP[step]}",
                                    reply_markup=calendar)

    async def task_cal(self, c):
        result, key, step = WYearTelegramCalendar(calendar_id=1, locale='ru').process(c.data)
        if not result and key:
            await self.bot.edit_message_text(f'Выбрать {LSTEP[step]}',
                                             c.message.chat.id,
                                             c.message.message_id,
                                             reply_markup=key)
        elif result:
            res = await self.repository.get_task_by_date(result)
            if res:
                await c.message.answer(res)
            else:
                await c.message.answer('На выбранный день нет заданий! Ура!')

    async def schedule_cal(self, c):
        result, key, step = DetailedTelegramCalendar(calendar_id=2, locale='ru').process(c.data)
        if not result and key:
            await self.bot.edit_message_text(f'Выбрать {LSTEP[step]}',
                                             c.message.chat.id,
                                             c.message.message_id,
                                             reply_markup=key)
        elif result:
            week = result.isocalendar()[1]
            res = await self.repository.get_schedule_by_week(week)
            if res:
                await c.message.answer(res)
            else:
                await c.message.answer('На выбранную неделю нет расписания :(')

    async def comment_cal(self, c):
        result, key, step = DetailedTelegramCalendar(calendar_id=3, locale='ru').process(c.data)
        if not result and key:
            await self.bot.edit_message_text(f'Выбрать {LSTEP[step]}',
                                             c.message.chat.id,
                                             c.message.message_id,
                                             reply_markup=key)
        elif result:
            week = result.isocalendar()[1]
            res = await self.repository.get_comment_by_week(week)
            if res:
                await c.message.answer(res)
            else:
                await c.message.answer('На выбранную неделю нет комментариев :(')

    async def train_results_cal(self, c):
        result, key, step = DetailedTelegramCalendar(calendar_id=4, locale='ru').process(c.data)
        if not result and key:
            await self.bot.edit_message_text(f'Выбрать {LSTEP[step]}',
                                             c.message.chat.id,
                                             c.message.message_id,
                                             reply_markup=key)
        elif result:
            week = result.isocalendar()[1]
            res = await self.repository.get_train_result_by_week(week)
            if res:
                await c.message.answer(res)
            else:
                await c.message.answer('На выбранную неделю нет результатов тренировок :(')

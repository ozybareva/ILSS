from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import date
from telegram_bot_calendar import DetailedTelegramCalendar

from logic.bot.keyboard import *
from persistance.repository import Repository
from settings import Settings

LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}


class ILSSBot:
    def __init__(self, settings: Settings, repository: Repository):
        self.bot = Bot(token=settings.api_token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.chat_id = settings.chat_id
        self.repository = repository
        self.register_handlers()

    def register_handlers(self):

        self.dp.register_message_handler(self.get_main_menu,
                                         commands=['start'])
        self.dp.register_message_handler(self.get_main_menu,
                                         text=ButtonText.BUTTON_MAIN_MENU)

        self.dp.register_message_handler(self.send_today_task_message,
                                         text=ButtonText.BUTTON_CURRENT_DAY_TEXT)
        self.dp.register_message_handler(self.send_current_week_schedule,
                                         text=ButtonText.BUTTON_CURRENT_WEEK_SCHEDULE_TEXT)
        self.dp.register_message_handler(self.select_date,
                                         text=ButtonText.BUTTON_SELECT_DATE)

        self.dp.register_message_handler(self.send_schedule_message_for_date,
                                         text=ButtonText.BUTTON_SCHEDULE_TEXT,
                                         state='*')
        self.dp.register_message_handler(self.send_task_message_for_date,
                                         text=ButtonText.BUTTON_TASK_TEXT,
                                         state='*')
        self.dp.register_message_handler(self.send_comments_message_for_date,
                                         text=ButtonText.BUTTON_COMMENT_TEXT,
                                         state='*')
        self.dp.register_message_handler(self.send_train_results_message_for_date,
                                         text=ButtonText.BUTTON_TRAIN_RESULTS_TEXT,
                                         state='*')

        self.dp.register_callback_query_handler(self.get_calendar, state='*')

    async def send_message(self, message: str):
        return await self.bot.send_message(chat_id=self.chat_id, text=message)

    async def unpin_messages(self):
        return await self.bot.unpin_all_chat_messages(chat_id=self.chat_id)

    async def pin_message(self, message_id: int):
        return await self.bot.pin_chat_message(chat_id=self.chat_id, message_id=message_id)

    async def get_main_menu(self, message: types.Message):
        keyboard = get_menu_keyboard()
        await message.answer('Выберите опцию', reply_markup=keyboard)

    async def send_today_task_message(self, message: types.Message):
        today_task = await self.repository.get_task_by_date(date.today()) or 'На сегодня нет заданий'
        await message.answer(today_task)

    async def send_current_week_schedule(self, message: types.Message):
        current_week_schedule = await self.repository.get_schedule_by_date(date.today()) or 'На текущую неделю нет плана'
        await message.answer(current_week_schedule)

    async def select_date(self, message: types.Message):
        calendar, step = DetailedTelegramCalendar(calendar_id=1, locale='ru').build()
        await self.bot.send_message(message.chat.id,
                                    f'Выбрать {LSTEP[step]}',
                                    reply_markup=calendar)

    async def get_calendar(self, c, state: FSMContext):
        result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru').process(c.data)
        if not result and key:
            await self.bot.edit_message_text(f'Выбрать {LSTEP[step]}',
                                             c.message.chat.id,
                                             c.message.message_id,
                                             reply_markup=key)
        elif result:
            await state.update_data(date=result)
            await self.get_options_menu(c.message, result)

    async def get_options_menu(self, message: types.Message, selected_date: date):
        keyboard = get_options_menu()
        await message.answer(f'Выберите опцию для даты {selected_date}', reply_markup=keyboard)

    async def send_task_message_for_date(self, message: types.Message, state: FSMContext):
        selected_date = await self.get_date_from_state(state)
        task = await self.repository.get_task_by_date(selected_date) or 'На выбранный день задания не найдено'
        await message.answer(task)

    async def send_schedule_message_for_date(self, message: types.Message, state: FSMContext):
        selected_date = await self.get_date_from_state(state)
        schedule = await self.repository.get_schedule_by_date(selected_date) or 'На выбранную неделю расписания не найдено'
        await message.answer(schedule)

    async def send_comments_message_for_date(self, message: types.Message, state: FSMContext):
        selected_date = await self.get_date_from_state(state)
        comments = await self.repository.get_comment_by_date(selected_date) or 'На выбранную неделю комментариев к плану не найдено'
        await message.answer(comments)

    async def send_train_results_message_for_date(self, message: types.Message, state: FSMContext):
        selected_date = await self.get_date_from_state(state)
        train_results = await self.repository.get_train_result_by_date(selected_date) \
                        or 'На выбранную неделю результатов тренировок и комментариев тренера не найдено'
        await message.answer(train_results)

    async def get_date_from_state(self, state: FSMContext):
        data = await state.get_data()
        return data.get('date')

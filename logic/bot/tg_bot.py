import datetime

from aiogram import Bot, Dispatcher, executor, types

from persistance.repository import Repository
from settings import Settings


class ILSSBot:
    def __init__(self, settings: Settings, repository: Repository):
        self.bot = Bot(token=settings.api_token)
        self.dp = Dispatcher(self.bot)
        self.repository = repository
        self.register_handler()

    def register_handler(self):
        self.dp.register_message_handler(self.start, commands=["start"])
        self.dp.register_message_handler(self.get_schedule, text=["Получить расписание на неделю"])
        self.dp.register_message_handler(self.get_task, text=["Получить задание на день"])

    async def send_message(self, chat_id: str, message: str):
        await self.bot.send_message(chat_id=chat_id, text=message)

    async def start(self, message: types.Message):
        kb = [
            [types.KeyboardButton(text="Получить расписание на неделю")],
            [types.KeyboardButton(text="Получить задание на день")],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Выберите опцию"
        )
        await message.answer("Выберите опцию", reply_markup=keyboard)

    async def get_schedule(self, message: types.Message):
        res = await self.repository.get_schedule()
        await message.answer(res)

    async def get_task(self, message: types.Message):
        res = await self.repository.get_task_by_date(date=datetime.datetime.now().date())
        await message.answer(res)
